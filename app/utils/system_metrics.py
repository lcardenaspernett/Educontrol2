# app/utils/system_metrics.py
"""
Utilidades para obtener métricas del sistema - Versión mejorada
Mantiene la simplicidad de tu código original pero con mejoras adicionales
"""
import os
import psutil
import shutil
from datetime import datetime
from flask import current_app
from app import db
from sqlalchemy import text

try:
    from app.models.audit_log import AuditLog
except ImportError:
    AuditLog = None

def format_bytes(bytes_value):
    """Formatear bytes en unidades legibles"""
    try:
        bytes_value = float(bytes_value)
        if bytes_value == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        
        while bytes_value >= 1024.0 and i < len(size_names) - 1:
            bytes_value /= 1024.0
            i += 1
        
        return f"{bytes_value:.1f} {size_names[i]}"
    except (ValueError, TypeError):
        return "0 B"

def get_database_size():
    """Obtiene el tamaño de la base de datos"""
    try:
        # Para SQLite
        if db.engine.url.drivername == 'sqlite':
            db_path = db.engine.url.database
            if db_path and os.path.exists(db_path):
                size_bytes = os.path.getsize(db_path)
                return format_bytes(size_bytes)
        
        # Para PostgreSQL
        elif db.engine.url.drivername == 'postgresql':
            try:
                result = db.session.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()))"))
                return result.fetchone()[0]
            except:
                return "N/A"
        
        # Para MySQL
        elif db.engine.url.drivername == 'mysql':
            try:
                result = db.session.execute(text("""
                    SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS 'size_mb'
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                """))
                size_mb = result.fetchone()[0]
                return f"{size_mb} MB" if size_mb else "0 MB"
            except:
                return "N/A"
        
        return "N/A"
    except Exception as e:
        print(f"Error obteniendo tamaño de BD: {e}")
        return "Error"

def get_active_connections():
    """Obtiene el número de conexiones activas a la base de datos"""
    try:
        # Para SQLite, siempre es 1
        if db.engine.url.drivername == 'sqlite':
            return 1
        
        # Para PostgreSQL
        elif db.engine.url.drivername == 'postgresql':
            try:
                result = db.session.execute(text("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"))
                return result.fetchone()[0]
            except:
                return "N/A"
        
        # Para MySQL
        elif db.engine.url.drivername == 'mysql':
            try:
                result = db.session.execute(text("SHOW STATUS LIKE 'Threads_connected'"))
                return result.fetchone()[1]
            except:
                return "N/A"
        
        # Fallback usando pool de conexiones
        try:
            return len(db.engine.pool._all_conns)
        except:
            return 1
            
    except Exception as e:
        print(f"Error obteniendo conexiones activas: {e}")
        return 0

def get_disk_space(metric='total'):
    """Obtiene información del espacio en disco"""
    try:
        # Usar la raíz del proyecto o '/' en sistemas Unix
        path = '/'
        if os.name == 'nt':  # Windows
            path = 'C:\\'
        
        total, used, free = shutil.disk_usage(path)
        
        if metric == 'total':
            return format_bytes(total)
        elif metric == 'used':
            return format_bytes(used)
        elif metric == 'free':
            return format_bytes(free)
        elif metric == 'percent':
            percent = (used / total) * 100
            return f"{percent:.1f}%"
        else:
            return {
                'total': format_bytes(total),
                'used': format_bytes(used),
                'free': format_bytes(free),
                'percent': f"{(used / total) * 100:.1f}%"
            }
    except Exception as e:
        print(f"Error obteniendo espacio en disco: {e}")
        return "Error" if metric in ['total', 'used', 'free', 'percent'] else {}

def get_memory_info(metric='total'):
    """Obtiene información de memoria"""
    try:
        mem = psutil.virtual_memory()
        
        if metric == 'total':
            return format_bytes(mem.total)
        elif metric == 'used':
            return format_bytes(mem.used)
        elif metric == 'free':
            return format_bytes(mem.available)
        elif metric == 'percent':
            return f"{mem.percent:.1f}%"
        else:
            return {
                'total': format_bytes(mem.total),
                'used': format_bytes(mem.used),
                'free': format_bytes(mem.available),
                'percent': f"{mem.percent:.1f}%"
            }
    except Exception as e:
        print(f"Error obteniendo información de memoria: {e}")
        return "Error" if metric in ['total', 'used', 'free', 'percent'] else {}

def get_cpu_usage():
    """Obtiene el uso de CPU"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        return f"{cpu_percent:.1f}%"
    except Exception as e:
        print(f"Error obteniendo uso de CPU: {e}")
        return "Error"

def get_last_backup_time():
    """Obtiene la fecha del último backup"""
    try:
        # Intentar obtener directorio desde configuración
        backup_dir = None
        
        try:
            backup_dir = current_app.config.get('BACKUP_DIR', 'backups')
        except:
            # Si no hay contexto de Flask, usar ruta relativa
            backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backups')
        
        if backup_dir and os.path.exists(backup_dir):
            files = [f for f in os.listdir(backup_dir) if f.endswith(('.sql', '.db', '.backup'))]
            if files:
                # Obtener el archivo más reciente
                latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(backup_dir, x)))
                backup_time = datetime.fromtimestamp(os.path.getctime(os.path.join(backup_dir, latest_file)))
                
                # Calcular tiempo transcurrido
                now = datetime.now()
                diff = now - backup_time
                
                if diff.days > 0:
                    return f"Hace {diff.days} días"
                elif diff.seconds > 3600:
                    hours = diff.seconds // 3600
                    return f"Hace {hours} horas"
                elif diff.seconds > 60:
                    minutes = diff.seconds // 60
                    return f"Hace {minutes} minutos"
                else:
                    return "Hace menos de 1 minuto"
        
        return 'No configurado'
    except Exception as e:
        print(f"Error obteniendo último backup: {e}")
        return 'Error'

def get_last_audit_log_time():
    """Obtiene la fecha del último registro de auditoría"""
    try:
        if AuditLog is None:
            return 'No configurado'
            
        latest_log = AuditLog.query.order_by(AuditLog.created_at.desc()).first()
        if latest_log:
            # Calcular tiempo transcurrido
            now = datetime.now()
            diff = now - latest_log.created_at
            
            if diff.days > 0:
                return f"Hace {diff.days} días"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"Hace {hours} horas"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"Hace {minutes} minutos"
            else:
                return "Hace menos de 1 minuto"
        
        return 'Sin registros'
    except Exception as e:
        print(f"Error obteniendo último audit log: {e}")
        return 'Error'

def get_system_uptime():
    """Obtiene el tiempo de actividad del sistema"""
    try:
        uptime_seconds = psutil.boot_time()
        boot_time = datetime.fromtimestamp(uptime_seconds)
        now = datetime.now()
        uptime = now - boot_time
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except Exception as e:
        print(f"Error obteniendo uptime: {e}")
        return "Error"

def get_process_count():
    """Obtiene el número de procesos del sistema"""
    try:
        return len(psutil.pids())
    except Exception as e:
        print(f"Error obteniendo número de procesos: {e}")
        return 0

def check_database_connection():
    """Verifica la conexión a la base de datos"""
    try:
        # Realizar una consulta simple
        db.session.execute(text("SELECT 1"))
        return {
            'status': 'connected',
            'message': 'Conexión exitosa'
        }
    except Exception as e:
        print(f"Error en conexión a BD: {e}")
        return {
            'status': 'error',
            'message': f'Error: {str(e)}'
        }

def get_comprehensive_system_info():
    """Obtiene información completa del sistema"""
    try:
        return {
            'timestamp': datetime.now().isoformat(),
            'database': {
                'connection': check_database_connection(),
                'size': get_database_size(),
                'connections': get_active_connections()
            },
            'system': {
                'cpu': get_cpu_usage(),
                'memory': get_memory_info(),
                'disk': get_disk_space(),
                'uptime': get_system_uptime(),
                'processes': get_process_count()
            },
            'backups': {
                'last_backup': get_last_backup_time(),
                'last_audit': get_last_audit_log_time()
            }
        }
    except Exception as e:
        print(f"Error obteniendo información del sistema: {e}")
        return {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

# Mantener compatibilidad con funciones originales
def get_last_backup_time_simple():
    """Versión simple original de get_last_backup_time"""
    try:
        backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backups')
        if os.path.exists(backup_dir):
            files = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
            if files:
                latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(backup_dir, x)))
                return datetime.fromtimestamp(os.path.getctime(os.path.join(backup_dir, latest_file))).strftime('%Y-%m-%d %H:%M:%S')
        return 'Nunca'
    except:
        return 'Nunca'

def get_last_audit_log_time_simple():
    """Versión simple original de get_last_audit_log_time"""
    try:
        if AuditLog is None:
            return 'Nunca'
        latest_log = AuditLog.query.order_by(AuditLog.created_at.desc()).first()
        if latest_log:
            return latest_log.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return 'Nunca'
    except:
        return 'Nunca'