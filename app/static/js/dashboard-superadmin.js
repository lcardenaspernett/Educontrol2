// Dashboard Superadmin JavaScript - Corregido para datos reales
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
                teachersData: [],
                roleLabels: ['Administradores', 'Profesores', 'Estudiantes', 'Padres'],
                roleData: [0, 0, 0, 0],
                monthlyGrowth: []
            },
            stats: {
                totalInstitutions: 0,
                totalUsers: 1,
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
            } else {
                number.textContent = '0';
            }
        });
    }

    // Función para crear gráfico de instituciones con datos reales
    function createInstitutionsChart() {
        const ctx = document.getElementById('institutionsChart');
        if (!ctx) {
            console.warn('Canvas para gráfico no encontrado');
            return;
        }

        // Usar datos reales del servidor
        let institutionNames = [];
        let studentsData = [];
        let teachersData = [];

        if (dashboardData.chartData && dashboardData.chartData.institutionNames.length > 0) {
            institutionNames = dashboardData.chartData.institutionNames;
            studentsData = dashboardData.chartData.studentsData;
            teachersData = dashboardData.chartData.teachersData;
        }

        // Si no hay datos, mostrar gráfico vacío con mensaje
        if (institutionNames.length === 0) {
            showEmptyChart(ctx);
            return;
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
                            stepSize: 1,
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
            showErrorChart(ctx);
        }
    }

    // Función para mostrar gráfico vacío cuando no hay datos
    function showEmptyChart(ctx) {
        const container = ctx.parentElement;
        container.innerHTML = `
            <div class="text-center p-5">
                <i class="fas fa-chart-bar text-muted mb-3" style="font-size: 3rem; opacity: 0.3;"></i>
                <h5 class="text-muted mb-2">No hay instituciones registradas</h5>
                <p class="text-muted mb-3">Comienza creando tu primera institución para ver los datos aquí</p>
                <a href="/superadmin/institution/create" class="btn btn-primary">
                    <i class="fas fa-plus me-2"></i>Crear Primera Institución
                </a>
            </div>
        `;
    }

    // Función para mostrar error en gráfico
    function showErrorChart(ctx) {
        const container = ctx.parentElement;
        container.innerHTML = `
            <div class="text-center p-4">
                <i class="fas fa-exclamation-triangle text-warning mb-3" style="font-size: 2rem;"></i>
                <p class="text-muted">Error cargando el gráfico</p>
                <button onclick="location.reload()" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-refresh me-1"></i>Intentar de nuevo
                </button>
            </div>
        `;
    }

    // Función para crear gráfico de roles con datos reales
    function createRolesChart() {
        const ctx = document.getElementById('rolesChart');
        if (!ctx) return;

        const roleLabels = dashboardData.chartData.roleLabels || ['Administradores', 'Profesores', 'Estudiantes', 'Padres'];
        const roleData = dashboardData.chartData.roleData || [0, 0, 0, 0];

        // Si todos los datos son 0, mostrar mensaje
        const totalUsers = roleData.reduce((sum, count) => sum + count, 0);
        if (totalUsers === 0) {
            showEmptyRolesChart(ctx);
            return;
        }

        const data = {
            labels: roleLabels,
            datasets: [{
                data: roleData,
                backgroundColor: [
                    'rgba(142, 45, 226, 0.8)',
                    'rgba(79, 172, 254, 0.8)',
                    'rgba(67, 233, 123, 0.8)',
                    'rgba(252, 74, 26, 0.8)'
                ],
                borderColor: [
                    'rgba(142, 45, 226, 1)',
                    'rgba(79, 172, 254, 1)',
                    'rgba(67, 233, 123, 1)',
                    'rgba(252, 74, 26, 1)'
                ],
                borderWidth: 2
            }]
        };

        const config = {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    },
                    title: {
                        display: true,
                        text: 'Distribución por Roles',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((sum, value) => sum + value, 0);
                                const percentage = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    duration: 1000
                }
            }
        };

        try {
            new Chart(ctx, config);
        } catch (error) {
            console.error('Error creando gráfico de roles:', error);
            showErrorChart(ctx);
        }
    }

    // Función para mostrar gráfico de roles vacío
    function showEmptyRolesChart(ctx) {
        const container = ctx.parentElement;
        container.innerHTML = `
            <div class="text-center p-4">
                <i class="fas fa-users text-muted mb-3" style="font-size: 2.5rem; opacity: 0.3;"></i>
                <h6 class="text-muted mb-2">Sin usuarios por roles</h6>
                <p class="text-muted small">Los datos aparecerán cuando agregues usuarios</p>
            </div>
        `;
    }

    // Función para crear gráfico de crecimiento mensual
    function createMonthlyGrowthChart() {
        const ctx = document.getElementById('monthlyGrowthChart');
        if (!ctx) return;

        const monthlyGrowth = dashboardData.chartData.monthlyGrowth || [];

        if (monthlyGrowth.length === 0) {
            showEmptyGrowthChart(ctx);
            return;
        }

        const labels = monthlyGrowth.map(item => item.month);
        const data = monthlyGrowth.map(item => item.users);

        const chartData = {
            labels: labels,
            datasets: [{
                label: 'Nuevos Usuarios',
                data: data,
                borderColor: 'rgba(142, 45, 226, 1)',
                backgroundColor: 'rgba(142, 45, 226, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(142, 45, 226, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        };

        const config = {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            font: {
                                size: 11
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        ticks: {
                            font: {
                                size: 11
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Crecimiento Mensual',
                        font: {
                            size: 14,
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
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        };

        try {
            new Chart(ctx, config);
        } catch (error) {
            console.error('Error creando gráfico de crecimiento:', error);
            showErrorChart(ctx);
        }
    }

    // Función para mostrar gráfico de crecimiento vacío
    function showEmptyGrowthChart(ctx) {
        const container = ctx.parentElement;
        container.innerHTML = `
            <div class="text-center p-4">
                <i class="fas fa-chart-line text-muted mb-3" style="font-size: 2.5rem; opacity: 0.3;"></i>
                <h6 class="text-muted mb-2">Sin datos de crecimiento</h6>
                <p class="text-muted small">El gráfico se poblará con el tiempo</p>
            </div>
        `;
    }

    // Función para descargar reportes (CORREGIDA)
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
        
        // Realizar descarga real
        fetch(`/superadmin/download-report/${type}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.blob();
            })
            .then(blob => {
                // Crear enlace de descarga
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `reporte_${type}_${new Date().toISOString().split('T')[0]}.csv`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                showNotification('Reporte descargado exitosamente', 'success');
            })
            .catch(error => {
                console.error('Error descargando reporte:', error);
                showNotification('Error al generar el reporte: ' + error.message, 'danger');
            })
            .finally(() => {
                // Restaurar botón
                button.innerHTML = originalText;
                button.disabled = false;
            });
    };

    // Función para actualizar dashboard con datos reales
    window.refreshDashboard = function() {
        const refreshBtn = document.querySelector('.refresh-btn i');
        if (refreshBtn) {
            refreshBtn.classList.add('fa-spin');
        }
        
        fetch('/superadmin/api/dashboard-data')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Actualizar estadísticas en las tarjetas
                    updateStatsCards(data.stats);
                    
                    // Actualizar información del sistema
                    updateSystemInfo(data.system_info);
                    
                    // Recrear gráficos con nuevos datos
                    dashboardData = data;
                    recreateCharts();
                    
                    showNotification('Dashboard actualizado correctamente', 'success');
                } else {
                    throw new Error(data.error || 'Error desconocido');
                }
            })
            .catch(error => {
                console.error('Error actualizando dashboard:', error);
                showNotification('Error al actualizar los datos: ' + error.message, 'danger');
            })
            .finally(() => {
                if (refreshBtn) {
                    refreshBtn.classList.remove('fa-spin');
                }
            });
    };

    // Función para actualizar las tarjetas de estadísticas
    function updateStatsCards(stats) {
        const updateCard = (selector, value) => {
            const element = document.querySelector(selector);
            if (element) {
                element.setAttribute('data-target', value);
                element.textContent = value.toLocaleString();
            }
        };

        // Buscar y actualizar cada tarjeta por su contenido o clase
        const cards = document.querySelectorAll('.stats-card');
        cards.forEach(card => {
            const numberElement = card.querySelector('.stats-number');
            const labelElement = card.querySelector('.stats-label');
            
            if (numberElement && labelElement) {
                const label = labelElement.textContent.toLowerCase();
                
                if (label.includes('instituciones')) {
                    numberElement.setAttribute('data-target', stats.total_institutions);
                    numberElement.textContent = stats.total_institutions.toLocaleString();
                } else if (label.includes('total usuarios')) {
                    numberElement.setAttribute('data-target', stats.total_users);
                    numberElement.textContent = stats.total_users.toLocaleString();
                } else if (label.includes('administradores')) {
                    numberElement.setAttribute('data-target', stats.total_admins);
                    numberElement.textContent = stats.total_admins.toLocaleString();
                } else if (label.includes('profesores')) {
                    numberElement.setAttribute('data-target', stats.total_teachers);
                    numberElement.textContent = stats.total_teachers.toLocaleString();
                } else if (label.includes('estudiantes')) {
                    numberElement.setAttribute('data-target', stats.total_students);
                    numberElement.textContent = stats.total_students.toLocaleString();
                } else if (label.includes('cursos')) {
                    numberElement.setAttribute('data-target', stats.total_courses);
                    numberElement.textContent = stats.total_courses.toLocaleString();
                }
            }
        });
    }

    // Función para actualizar información del sistema
    function updateSystemInfo(systemInfo) {
        // Actualizar usuarios conectados
        const connectedUsersElement = document.getElementById('connected-users');
        if (connectedUsersElement && systemInfo.connected_users !== undefined) {
            connectedUsersElement.textContent = systemInfo.connected_users;
        }
        
        // Actualizar otros elementos del sistema si existen
        // ... más actualizaciones según sea necesario
    }

    // Función para recrear todos los gráficos
    function recreateCharts() {
        // Limpiar contenedores de gráficos
        const chartContainers = ['institutionsChart', 'rolesChart', 'monthlyGrowthChart'];
        chartContainers.forEach(id => {
            const container = document.getElementById(id);
            if (container && container.parentElement) {
                // Crear nuevo canvas
                const newCanvas = document.createElement('canvas');
                newCanvas.id = id;
                container.parentElement.replaceChild(newCanvas, container);
            }
        });
        
        // Recrear gráficos
        setTimeout(() => {
            createInstitutionsChart();
            createRolesChart();
            createMonthlyGrowthChart();
        }, 100);
    }

    // Función para manejar clics en las tarjetas de estadísticas
    function setupStatsCardClicks() {
        const statsCards = document.querySelectorAll('.stats-card[onclick]');
        
        statsCards.forEach(card => {
            card.addEventListener('click', function() {
                // Efecto visual de clic
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }

    // Función para mostrar notificaciones
    function showNotification(message, type) {
        type = type || 'info';
        
        // Crear contenedor de notificaciones si no existe
        let notificationContainer = document.getElementById('notification-overlay');
        if (!notificationContainer) {
            notificationContainer = document.createElement('div');
            notificationContainer.id = 'notification-overlay';
            
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
            
            document.body.appendChild(notificationContainer);
        }

        // Crear la notificación
        const notification = document.createElement('div');
        
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
        
        // Mostrar animación
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
                    
                    if (notificationContainer && notificationContainer.children.length === 0) {
                        notificationContainer.remove();
                    }
                }, 300);
            }
        }, 5000);
    }

    // Inicializar funcionalidades del dashboard
    function initDashboard() {
        // Ejecutar animaciones de números
        setTimeout(animateNumbers, 500);
        
        // Crear gráficos
        setTimeout(() => {
            createInstitutionsChart();
            createRolesChart();
            createMonthlyGrowthChart();
        }, 1000);
        
        // Configurar eventos de tarjetas
        setupStatsCardClicks();
        
        console.log('Dashboard del Superadmin inicializado correctamente con datos reales');
    }

    // Ejecutar inicialización
    initDashboard();

    // Exponer funciones globales
    window.DashboardSuperadmin = {
        animateNumbers: animateNumbers,
        createChart: createInstitutionsChart,
        showNotification: showNotification,
        downloadReport: window.downloadReport,
        refreshDashboard: window.refreshDashboard
    };
});