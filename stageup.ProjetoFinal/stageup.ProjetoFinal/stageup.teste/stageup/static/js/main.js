// Main JavaScript file for StageUp

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.transition = 'opacity 0.5s';
            flash.style.opacity = '0';
            setTimeout(function() {
                flash.remove();
            }, 500);
        }, 5000);
    });

    // Carrossel de Vagas
    const carouselWrapper = document.getElementById('carouselWrapper');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const carouselDots = document.getElementById('carouselDots');
    
    if (carouselWrapper) {
        const items = carouselWrapper.querySelectorAll('.carousel-item');
        const totalItems = items.length;
        let currentIndex = 0;
        
        function getItemsPerView() {
            if (window.innerWidth >= 1024) return 3;
            if (window.innerWidth >= 768) return 2;
            return 1;
        }
        
        let itemsPerView = getItemsPerView();
        let maxIndex = Math.max(0, totalItems - itemsPerView);
        
        // Criar dots
        if (carouselDots && totalItems > itemsPerView) {
            for (let i = 0; i <= maxIndex; i++) {
                const dot = document.createElement('button');
                dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
                dot.setAttribute('aria-label', `Ir para slide ${i + 1}`);
                dot.addEventListener('click', () => goToSlide(i));
                carouselDots.appendChild(dot);
            }
        }
        
        function updateCarousel() {
            const itemWidth = items[0]?.offsetWidth || 320;
            const gap = 24; // 1.5rem = 24px
            const translateX = -(currentIndex * (itemWidth + gap));
            carouselWrapper.style.transform = `translateX(${translateX}px)`;
            
            // Atualizar botões
            if (prevBtn) prevBtn.disabled = currentIndex === 0;
            if (nextBtn) nextBtn.disabled = currentIndex >= maxIndex;
            
            // Atualizar dots
            if (carouselDots) {
                const dots = carouselDots.querySelectorAll('.carousel-dot');
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === currentIndex);
                });
            }
        }
        
        function goToSlide(index) {
            currentIndex = Math.max(0, Math.min(index, maxIndex));
            updateCarousel();
        }
        
        function nextSlide() {
            if (currentIndex < maxIndex) {
                currentIndex++;
                updateCarousel();
            }
        }
        
        function prevSlide() {
            if (currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        }
        
        if (prevBtn) prevBtn.addEventListener('click', prevSlide);
        if (nextBtn) nextBtn.addEventListener('click', nextSlide);
        
        // Inicializar
        updateCarousel();
        
        // Auto-play (opcional)
        let autoPlayInterval;
        function startAutoPlay() {
            autoPlayInterval = setInterval(() => {
                if (currentIndex >= maxIndex) {
                    currentIndex = 0;
                } else {
                    currentIndex++;
                }
                updateCarousel();
            }, 5000);
        }
        
        function stopAutoPlay() {
            if (autoPlayInterval) {
                clearInterval(autoPlayInterval);
            }
        }
        
        // Pausar auto-play ao passar o mouse
        if (carouselWrapper) {
            carouselWrapper.addEventListener('mouseenter', stopAutoPlay);
            carouselWrapper.addEventListener('mouseleave', startAutoPlay);
            startAutoPlay();
        }
        
        // Atualizar ao redimensionar
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                itemsPerView = getItemsPerView();
                maxIndex = Math.max(0, totalItems - itemsPerView);
                if (currentIndex > maxIndex) {
                    currentIndex = maxIndex;
                }
                updateCarousel();
                
                // Recriar dots se necessário
                if (carouselDots) {
                    carouselDots.innerHTML = '';
                    if (totalItems > itemsPerView) {
                        for (let i = 0; i <= maxIndex; i++) {
                            const dot = document.createElement('button');
                            dot.className = 'carousel-dot' + (i === currentIndex ? ' active' : '');
                            dot.setAttribute('aria-label', `Ir para slide ${i + 1}`);
                            dot.addEventListener('click', () => goToSlide(i));
                            carouselDots.appendChild(dot);
                        }
                    }
                }
            }, 250);
        });
    }

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Basic validation
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#EF4444';
                } else {
                    field.style.borderColor = '';
                }
            });

            // Password confirmation check
            const password = form.querySelector('#password');
            const confirmPassword = form.querySelector('#confirm_password');
            if (password && confirmPassword) {
                if (password.value !== confirmPassword.value) {
                    isValid = false;
                    confirmPassword.style.borderColor = '#EF4444';
                    alert('As senhas não coincidem!');
                }
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

