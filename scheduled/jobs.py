import os
import threading
import time
from shared.time import now
from instance.database import db

def scheduled_job_setup(app):
    def background_worker():
        """Runs in a loop forever"""
        while True:
            with app.app_context():
                try:
                    app.logger.info(f"Starting background task at {now()}")

                    # Example task: Update product ratings
                    from models.product import Product

                    products = Product.query.all()
                    for product in products:
                        product.update_rating_stats()
                    db.session.commit()
                    app.logger.info(f"Updated {len(products)} products")

                except Exception as e:
                    app.logger.error(f"Background task failed: {str(e)}")
                    db.session.rollback()

            time.sleep(300)  # 5 minutes

    # New way to initialize worker in Flask 2.3+
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        # Check if thread already exists
        if not any(t.name == "BackgroundWorker" for t in threading.enumerate()):
            thread = threading.Thread(
                target=background_worker, daemon=True, name="BackgroundWorker"
            )
            thread.start()
            app.logger.info("Background worker initialized")

    # Monitoring endpoint
    @app.route("/task-status")
    def task_status():
        is_alive = any(
            t.name == "BackgroundWorker" and t.is_alive() for t in threading.enumerate()
        )
        return {
            "status": "running" if is_alive else "stopped",
            "thread_count": threading.active_count(),
            "threads": [t.name for t in threading.enumerate()],
        }