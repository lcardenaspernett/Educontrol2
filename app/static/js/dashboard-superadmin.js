// Dashboard Superadmin JavaScript
// Archivo: app/static/js/dashboard-superadmin.js

document.addEventListener('DOMContentLoaded', function() {
    // Obtener datos del JSON embebido
    let dashboardData = {};
    try {
        const dataScript = document.getElementById('dashboard-data');
        if (dataScript) {
            dashboardData = JSON.parse(dataScript.textContent);
        }
    } catch (error) {
        console.warn('No se pudieron cargar los datos del dashboard:', error);
        dashboardData = {
            chartData: {
                institutionNames: [],
                studentsData: [],
                teachersData: []
            },
            stats: {
                totalInstitutions: 0,
                totalUsers: 0,
                totalAdmins: 0,
                totalTeachers: 0,
                totalStudents: 0,
                totalCourses: 0
            }
        };
    }

    // Función para animar números
    function animateNumbers() {
        const statNumbers = document.querySelectorAll('.stats-number[data-target]');
        
        statNumbers.forEach(number => {
            const targetValue = parseInt(number.getAttribute('data-target')) || 0;
            const duration = 2000;
            const startTime = Date.now();
            
            function updateNumber() {
                const elapsed = Date.now() - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const currentValue = Math.round(targetValue * progress);
                
                if (currentValue >= 1000) {
                    number.textContent = currentValue.toLocaleString();
                } else {
                    number.textContent = currentValue;
                }
                
                if (progress < 1) {
                    requestAnimationFrame(updateNumber);
                }
            }
            
            if (targetValue > 0) {
                number.textContent = '0';
                requestAnimationFrame(updateNumber);
            }
        });
    }

    // Función para crear gráfico de instituciones
    function createInstitutionsChart() {
        const ctx = document.getElementById('institutionsChart');
        if (!ctx) {
            console.warn('Canvas para gráfico no encontrado');
            return;
        }

        // Usar datos del servidor o datos de ejemplo
        let institutionNames = ['Instituto A', 'Colegio B', 'Universidad C', 'Escuela D', 'Liceo E'];
        let studentsData = [120, 85, 200, 67, 150];
        let teachersData = [12, 8, 25, 7, 18];

        // Verificar si hay datos del servidor
        if (dashboardData.chartData) {
            if (dashboardData.chartData.institutionNames && dashboardData.chartData.institutionNames.length > 0) {
                institutionNames = dashboardData.chartData.institutionNames;
            }
            if (dashboardData.chartData.studentsData && dashboardData.chartData.studentsData.length > 0) {
                studentsData = dashboardData.chartData.studentsData;
            }
            if (dashboardData.chartData.teachersData && dashboardData.chartData.teachersData.length > 0) {
                teachersData = dashboardData.chartData.teachersData;
            }
        }

        const data = {
            labels: institutionNames,
            datasets: [{
                label: 'Estudiantes',
                data: studentsData,
                backgroundColor: 'rgba(142, 45, 226, 0.6)',
                borderColor: 'rgba(142, 45, 226, 1)',
                borderWidth: 2,
                borderRadius: 4,
                borderSkipped: false
            }, {
                label: 'Profesores', 
                data: teachersData,
                backgroundColor: 'rgba(74, 0, 224, 0.6)',
                borderColor: 'rgba(74, 0, 224, 1)',
                borderWidth: 2,
                borderRadius: 4,
                borderSkipped: false
            }]
        };

        const config = {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    title: {
                        display: true,
                        text: 'Distribución de Usuarios por Institución',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: 'rgba(142, 45, 226, 1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 12
                            }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            stepSize: 10,
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        };

        // Crear el gráfico
        try {
            new Chart(ctx, config);
        } catch (error) {
            console.error('Error creando el gráfico:', error);
            // Mostrar mensaje de error en el canvas
            const container = ctx.parentElement;
            container.innerHTML = '<div class="text-center p-4"><i class="fas fa-exclamation-triangle text-warning"></i><br>Error cargando el gráfico</div>';
        }
    }

    // Función para descargar reportes
    window.downloadReport = function(type) {
        const reportTypes = {
            'institutions': 'Reporte de Instituciones',
            'users': 'Reporte de Usuarios', 
            'activity': 'Log de Actividades',
            'full': 'Reporte Completo del Sistema'
        };
        
        // Mostrar loading
        const button = event.target.closest('button');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generando...';
        button.disabled = true;
        
        // Simular descarga (en implementación real, esto sería una llamada al servidor)
        setTimeout(() => {
            alert('Descargando: ' + reportTypes[type] + '\n\nEn una implementación real, esto generaría y descargaría el archivo.');
            
            // Restaurar botón
            button.innerHTML = originalText;
            button.disabled = false;
            
            // En la implementación real, harías algo como:
            // window.location.href = '/superadmin/download-report/' + type;
        }, 1500);
    };

    // Función para manejar clics en las tarjetas de estadísticas
    function setupStatsCardClicks() {
        const statsCards = document.querySelectorAll('.stats-card');
        
        statsCards.forEach(card => {
            card.addEventListener('click', function() {
                // Efecto visual de clic
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
                
                // Aquí puedes agregar navegación específica según el tipo de tarjeta
                if (this.classList.contains('institutions')) {
                    console.log('Navegar a gestión de instituciones');
                    // window.location.href = '/superadmin/institutions';
                } else if (this.classList.contains('users')) {
                    console.log('Navegar a gestión de usuarios');
                    // window.location.href = '/superadmin/users';
                } else if (this.classList.contains('teachers')) {
                    console.log('Navegar a gestión de profesores');
                    // window.location.href = '/superadmin/teachers';
                } else if (this.classList.contains('students')) {
                    console.log('Navegar a gestión de estudiantes');
                    // window.location.href = '/superadmin/students';
                }
            });
        });
    }

    // Función para mostrar notificaciones que NO mueven el dashboard
    function showNotification(message, type) {
        type = type || 'info';
        
        // Crear contenedor de notificaciones si no existe
        let notificationContainer = document.getElementById('notification-overlay');
        if (!notificationContainer) {
            notificationContainer = document.createElement('div');
            notificationContainer.id = 'notification-overlay';
            
            // Estilos que NO afectan el layout del documento
            notificationContainer.style.cssText = 
                'position: fixed !important;' +
                'top: 80px !important;' +
                'right: 20px !important;' +
                'z-index: 999999 !important;' +
                'width: 350px !important;' +
                'max-height: calc(100vh - 100px) !important;' +
                'overflow-y: auto !important;' +
                'pointer-events: none !important;' +
                'margin: 0 !important;' +
                'padding: 0 !important;' +
                'border: none !important;' +
                'background: transparent !important;';
            
            // Agregar directamente al body al final
            document.body.appendChild(notificationContainer);
        }

        // Crear la notificación
        const notification = document.createElement('div');
        
        // Estilos inline para evitar conflictos con CSS existente
        notification.style.cssText = 
            'margin-bottom: 10px !important;' +
            'padding: 12px 16px !important;' +
            'border-radius: 8px !important;' +
            'box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;' +
            'border: none !important;' +
            'font-size: 14px !important;' +
            'font-weight: 500 !important;' +
            'pointer-events: auto !important;' +
            'transform: translateX(100%) !important;' +
            'transition: all 0.3s ease !important;' +
            'opacity: 0 !important;' +
            'position: relative !important;' +
            'display: flex !important;' +
            'align-items: center !important;' +
            'justify-content: space-between !important;' +
            'min-height: 50px !important;' +
            'width: 100% !important;' +
            'box-sizing: border-box !important;';
        
        // Colores según el tipo
        const colors = {
            'success': 'background: #10b981 !important; color: white !important;',
            'danger': 'background: #ef4444 !important; color: white !important;',
            'warning': 'background: #f59e0b !important; color: white !important;',
            'info': 'background: #3b82f6 !important; color: white !important;'
        };
        
        notification.style.cssText += colors[type] || colors.info;
        
        // Iconos según el tipo
        const icons = {
            'success': '✅',
            'danger': '🚨',
            'warning': '⚠️',
            'info': 'ℹ️'
        };
        
        // Contenido de la notificación
        notification.innerHTML = 
            '<div style="display: flex; align-items: center; flex: 1; margin-right: 10px;">' +
                '<span style="margin-right: 8px; font-size: 16px;">' + (icons[type] || icons.info) + '</span>' +
                '<span style="flex: 1;">' + message + '</span>' +
            '</div>' +
            '<button onclick="this.parentElement.remove()" style="' +
                'background: transparent !important;' +
                'border: none !important;' +
                'color: white !important;' +
                'font-size: 18px !important;' +
                'cursor: pointer !important;' +
                'padding: 0 !important;' +
                'margin: 0 !important;' +
                'line-height: 1 !important;' +
                'opacity: 0.7 !important;' +
                'width: 20px !important;' +
                'height: 20px !important;' +
                'display: flex !important;' +
                'align-items: center !important;' +
                'justify-content: center !important;' +
            '">×</button>';
        
        // Agregar al contenedor
        notificationContainer.appendChild(notification);
        
        // Forzar repaint y mostrar
        requestAnimationFrame(function() {
            notification.style.transform = 'translateX(0) !important';
            notification.style.opacity = '1 !important';
        });
        
        // Auto-remover después de 5 segundos
        setTimeout(function() {
            if (notification.parentNode) {
                notification.style.transform = 'translateX(100%) !important';
                notification.style.opacity = '0 !important';
                
                setTimeout(function() {
                    if (notification.parentNode) {
                        notification.remove();
                    }
                    
                    // Limpiar contenedor si está vacío
                    if (notificationContainer && notificationContainer.children.length === 0) {
                        notificationContainer.remove();
                    }
                }, 300);
            }
        }, 5000);
    }

    // Función para probar notificaciones
    window.testNotifications = function() {
        const notifications = [
            { message: 'Sistema funcionando correctamente', type: 'success' },
            { message: 'Uso de almacenamiento alto (85%)', type: 'warning' },
            { message: 'Nuevo usuario registrado: María García', type: 'info' },
            { message: 'Error de conexión detectado', type: 'danger' }
        ];

        notifications.forEach(function(notif, index) {
            setTimeout(function() {
                showNotification(notif.message, notif.type);
            }, index * 500);
        });
    };

    // Función para actualizar estadísticas en tiempo real (opcional)
    function updateStatsInRealTime() {
        // Esta función se puede llamar periódicamente para actualizar estadísticas
        // Ejemplo: hacer una llamada AJAX cada 30 segundos
        
        // fetch('/api/superadmin/stats')
        //     .then(response => response.json())
        //     .then(data => {
        //         // Actualizar números en las tarjetas
        //         updateStatsCards(data);
        //     })
        //     .catch(error => {
        //         console.error('Error actualizando estadísticas:', error);
        //     });
    }

    // Función para verificar el estado del sistema
    function checkSystemHealth() {
        // Simular verificación de salud del sistema
        const indicators = [
            { name: 'Servidor', status: 'healthy' },
            { name: 'Base de Datos', status: 'healthy' },
            { name: 'API', status: 'healthy' },
            { name: 'Almacenamiento', status: 'warning' } // Ejemplo de advertencia
        ];
        
        indicators.forEach(function(indicator) {
            if (indicator.status === 'warning') {
                showNotification('Advertencia en ' + indicator.name + ': Uso de almacenamiento alto', 'warning');
            } else if (indicator.status === 'error') {
                showNotification('Error en ' + indicator.name + ': Requiere atención inmediata', 'danger');
            }
        });
    }

    // Inicializar funcionalidades
    function initDashboard() {
        // Ejecutar animaciones
        setTimeout(animateNumbers, 500);
        
        // Crear gráfico
        setTimeout(createInstitutionsChart, 1000);
        
        // Configurar eventos de tarjetas
        setupStatsCardClicks();
        
        // Verificar salud del sistema (opcional)
        // setTimeout(checkSystemHealth, 2000);
        
        // Actualizar estadísticas cada 30 segundos (opcional)
        // setInterval(updateStatsInRealTime, 30000);
        
        console.log('Dashboard del Superadmin inicializado correctamente');
    }

    // Ejecutar inicialización
    initDashboard();

    // Exponer funciones globales si es necesario
    window.DashboardSuperadmin = {
        animateNumbers: animateNumbers,
        createChart: createInstitutionsChart,
        showNotification: showNotification,
        downloadReport: window.downloadReport
    };
});