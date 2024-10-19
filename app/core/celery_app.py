from celery import Celery

# Crear la instancia de Celery
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Ajusta si es necesario
    backend="redis://localhost:6379/0"  # Ajusta si es necesario
)

# Configuración adicional (opcional)
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Solo acepta JSON
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery_app.autodiscover_tasks(['app. core']) 