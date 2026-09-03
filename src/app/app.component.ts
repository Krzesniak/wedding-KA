import { AfterViewInit, Component, ElementRef, OnDestroy, ViewChild, signal } from '@angular/core';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements AfterViewInit, OnDestroy {
  @ViewChild('page') private page?: ElementRef<HTMLElement>;
  protected readonly started = signal(false);
  private context?: gsap.Context;

  ngAfterViewInit(): void { gsap.registerPlugin(ScrollTrigger); }

  protected startStory(): void {
    this.started.set(true);
    requestAnimationFrame(() => requestAnimationFrame(() => this.buildAnimations()));
  }

  private buildAnimations(): void {
    const root = this.page?.nativeElement;
    if (!root) return;
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) return;

    this.context = gsap.context(() => {
      gsap.timeline()
        .to('.intro__glow', { opacity: .75, duration: 1.5, ease: 'power2.out' })
        .from('.rings-photo', { y: 55, scale: .62, rotation: -7, opacity: 0, duration: 1.9, ease: 'power3.out' }, '-=.6')
        .to('.rings-photo', { scale: 1.055, duration: .75, yoyo: true, repeat: 1 })
        .fromTo('.rings-photo__shine', { xPercent: -170, opacity: 0 }, { xPercent: 190, opacity: .9, duration: 1.15 }, '-=1.15')
        .from('.intro__copy > *', { y: 28, opacity: 0, duration: .95, stagger: .18 }, '-=.65')
        .from('.intro__scroll', { opacity: 0, y: -10, duration: .7 });

      gsap.utils.toArray<HTMLElement>('[data-reveal]').forEach((node) => {
        gsap.from(node, {
          opacity: 0, y: 48, duration: 1, ease: 'power3.out',
          scrollTrigger: { trigger: node, start: 'top 84%', once: true }
        });
      });

      gsap.from('.wall__karol', {
        x: -150, opacity: 0, rotation: -5, duration: 1.25,
        scrollTrigger: { trigger: '.wall-scene', start: 'top 72%', once: true }
      });

      gsap.timeline({ scrollTrigger: { trigger: '.swipe-scene', start: 'top 68%', once: true } })
        .from('.phone', { y: 80, opacity: 0, rotation: -4, duration: .9 }, '-=.45')
        .from('.profile-card', { scale: .86, opacity: 0, duration: .7 }, '-=.25')
        .to('.profile-card', { x: 300, rotation: 18, opacity: 0, duration: 1.1, delay: .55, ease: 'power2.in' })
        .from('.match', { scale: .4, opacity: 0, duration: .75, ease: 'back.out(1.8)' }, '-=.2');


      gsap.timeline({ scrollTrigger: { trigger: '.kiss-scene', start: 'top 68%', once: true } })
        .from('.anime-character--ania', { xPercent: -170, opacity: 0, duration: 1.25, ease: 'power3.out' })
        .from('.anime-character--karol', { xPercent: 170, opacity: 0, duration: 1.25, ease: 'power3.out' }, '<')
        .to('.anime-character--ania', { xPercent: 42, rotation: 2, duration: 1.1, ease: 'power2.inOut' })
        .to('.anime-character--karol', { xPercent: -42, rotation: -2, duration: 1.1, ease: 'power2.inOut' }, '<')
        .to('.anime-character', { opacity: 0, scale: .92, duration: .45 })
        .fromTo('.anime-hug-final', { opacity: 0, scale: .82 }, { opacity: 1, scale: 1, duration: .8, ease: 'back.out(1.45)' }, '-=.25')
        .from('.floating-hearts > *', { y: 45, scale: 0, opacity: 0, rotation: -25, duration: .75, stagger: .12, ease: 'back.out(2)' }, '-=.38')
        .to('.floating-hearts span', { y: -18, duration: 1.3, yoyo: true, repeat: -1, stagger: .16, ease: 'sine.inOut' });

      gsap.timeline({ scrollTrigger: { trigger: '.date-scene', start: 'top 72%', once: true } })
        .from('.date-scene__line', { scaleX: 0, duration: 1.2, transformOrigin: 'left' })
        .from('.date-scene__date', { opacity: 0, scale: .75, duration: .8, ease: 'back.out(1.6)' })
        .from('.date-scene__copy', { opacity: 0, y: 20, duration: .7 });

      gsap.from('.future__item', {
        opacity: 0, y: 30, scale: .8, duration: .7, stagger: .16,
        scrollTrigger: { trigger: '.future', start: 'top 65%', once: true }
      });
    }, root);
    ScrollTrigger.refresh();
  }

  ngOnDestroy(): void { this.context?.revert(); ScrollTrigger.getAll().forEach(trigger => trigger.kill()); }
}
