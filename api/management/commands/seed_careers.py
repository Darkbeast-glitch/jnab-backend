from django.core.management.base import BaseCommand
from api.models import JobPosition


class Command(BaseCommand):
    help = "Seeds initial career openings for JNAB Innovations"

    def handle(self, *args, **options):
        initial_positions = [
            {
                "title": "Senior Full-Stack Engineer (React & Django/Python)",
                "slug": "senior-full-stack-engineer",
                "department": "engineering",
                "location": "Accra, Ghana · Global Remote",
                "work_type": "remote",
                "employment_type": "full_time",
                "experience_level": "Senior (4+ yrs)",
                "salary_range": "$28,000 – $48,000 / yr + Performance Bonus",
                "featured": True,
                "summary": "Lead the architecture and implementation of resilient, high-throughput web applications for international startups and African scale-ups.",
                "description": "We are seeking an exceptional Senior Full-Stack Engineer who thrives on building mission-critical platforms. You will work across modern React/TypeScript frontends and high-performance Python/Django REST API backends, designing distributed architectures, caching layers, and database schemas that scale to millions of users.",
                "responsibilities": (
                    "• Architect and develop scalable web platforms using React, TypeScript, Python, and Django REST Framework.\n"
                    "• Own features from technical specification to production release, ensuring 99.98% SLA reliability.\n"
                    "• Collaborate with product designers and client CTOs to scope, estimate, and build bespoke digital solutions.\n"
                    "• Mentor fellows from JNAB Academy and conduct rigorous peer code reviews."
                ),
                "requirements": (
                    "• 4+ years of professional full-stack development experience.\n"
                    "• Deep mastery of React, TypeScript, Next.js, and modern state management.\n"
                    "• Strong experience with Python, Django, PostgreSQL, Redis, and RESTful API architecture.\n"
                    "• Proven ability to design performant database queries and microservices.\n"
                    "• Experience with Docker, CI/CD pipelines, and cloud deployments (AWS / GCP)."
                ),
                "benefits": "Remote-first culture, top-tier MacBook Pro setup, comprehensive health coverage, annual learning & conference stipend, performance equity."
            },
            {
                "title": "Lead Mobile Application Engineer (Flutter / iOS / Android)",
                "slug": "lead-mobile-application-engineer",
                "department": "engineering",
                "location": "Accra Tech Hub / Hybrid Remote",
                "work_type": "hybrid",
                "employment_type": "full_time",
                "experience_level": "Lead (5+ yrs)",
                "salary_range": "$30,000 – $52,000 / yr + Tech Allowance",
                "featured": True,
                "summary": "Architect cross-platform mobile experiences with offline-first capabilities, biometric security, and sub-second transaction speed.",
                "description": "Lead JNAB's mobile engineering guild. You will architect flagship iOS and Android applications using Flutter and native integrations, delivering enterprise-grade performance, fluid 60fps animations, and military-grade security.",
                "responsibilities": (
                    "• Lead mobile engineering for client scale-up projects across FinTech, HealthTech, and Logistics.\n"
                    "• Architect robust offline-first synchronization, push notification pipelines, and biometric auth.\n"
                    "• Oversee App Store and Google Play publishing and automated CI/CD release pipelines.\n"
                    "• Establish mobile testing standards (unit, widget, and end-to-end integration tests)."
                ),
                "requirements": (
                    "• 4+ years dedicated experience with Flutter & Dart, plus familiarity with Swift/Kotlin.\n"
                    "• Experience shipping consumer-facing mobile applications with 100K+ downloads.\n"
                    "• Strong understanding of reactive programming (Bloc, Riverpod, or Provider).\n"
                    "• Experience with secure storage, encryption, and payment gateway SDK integrations."
                ),
                "benefits": "Flexible hybrid hours, modern innovation hub in Accra, health insurance, home-office equipment budget."
            },
            {
                "title": "Senior Product Designer (UI/UX & Design Systems)",
                "slug": "senior-product-designer",
                "department": "design",
                "location": "Global Remote · Accra Timezone (GMT)",
                "work_type": "remote",
                "employment_type": "full_time",
                "experience_level": "Senior (4+ yrs)",
                "salary_range": "$24,000 – $42,000 / yr",
                "featured": True,
                "summary": "Craft editorial, high-converting digital interfaces, comprehensive tokenized design systems, and intuitive user experiences.",
                "description": "Join our design studio to shape digital products for ambitious brands. You will translate ambiguous business requirements into wireframes, interactive prototypes, and production-ready design systems that engineering pods love building.",
                "responsibilities": (
                    "• Lead end-to-end product design from user research and journey mapping to high-fidelity Figma files.\n"
                    "• Build, maintain, and evolve tokenized design systems and component libraries.\n"
                    "• Conduct usability testing sessions with real users across West African and international markets.\n"
                    "• Work closely with frontend engineers to ensure pixel-perfect fidelity across responsive viewports."
                ),
                "requirements": (
                    "• 4+ years designing production web and mobile software.\n"
                    "• Exceptional portfolio showcasing clean typography, interaction design, and design systems.\n"
                    "• Expert mastery of Figma, auto-layout, component variants, and interactive prototyping.\n"
                    "• Strong grasp of frontend accessibility (WCAG), CSS grid, and responsive web principles."
                ),
                "benefits": "Figma Enterprise license, design books & course budget, remote flexibility, health insurance."
            },
            {
                "title": "Cloud Infrastructure & DevOps Engineer (AWS / Kubernetes)",
                "slug": "cloud-infrastructure-devops-engineer",
                "department": "engineering",
                "location": "Accra, Ghana · Remote",
                "work_type": "remote",
                "employment_type": "full_time",
                "experience_level": "Mid – Senior (3+ yrs)",
                "salary_range": "$26,000 – $45,000 / yr",
                "featured": False,
                "summary": "Design automated multi-environment CI/CD pipelines, container orchestration, and 99.98% uptime cloud infrastructure.",
                "description": "Own JNAB's cloud foundation and client deployment pipelines. You will configure AWS, Docker, Kubernetes, and automated observability platforms to ensure our applications run securely and seamlessly at scale.",
                "responsibilities": (
                    "• Provision and maintain infrastructure as code (Terraform / CloudFormation) on AWS.\n"
                    "• Build automated GitHub Actions CI/CD workflows for linting, testing, and container deployment.\n"
                    "• Implement logging, APM, and alerting with Prometheus, Grafana, and Sentry.\n"
                    "• Enforce security best practices, secrets management, and automated vulnerability scanning."
                ),
                "requirements": (
                    "• 3+ years experience managing cloud infrastructure (AWS preferred).\n"
                    "• Strong hands-on experience with Docker, Kubernetes, Nginx, and Linux system administration.\n"
                    "• Proficient in bash scripting and Python automation.\n"
                    "• Understanding of zero-downtime blue/green or rolling deployments."
                ),
                "benefits": "AWS certification sponsorship, remote stipend, flexible working arrangements."
            },
            {
                "title": "Technical Training Lead (JNAB Academy)",
                "slug": "technical-training-lead-academy",
                "department": "talent",
                "location": "Accra Tech Hub / Hybrid",
                "work_type": "hybrid",
                "employment_type": "full_time",
                "experience_level": "Senior (4+ yrs)",
                "salary_range": "$22,000 – $38,000 / yr",
                "featured": False,
                "summary": "Direct our curriculum, mentor emerging engineering fellows, and build Ghana's premier tech talent pipeline.",
                "description": "Inspire and cultivate the next generation of African tech leaders. You will design hands-on project-based curriculums, mentor Academy fellows through real-world software builds, and evaluate readiness for global tech squad placements.",
                "responsibilities": (
                    "• Oversee the Full-Stack and Product Design training curriculums for JNAB Academy.\n"
                    "• Lead live technical workshops, code critiques, and architecture teardowns.\n"
                    "• Manage fellow progression, assessments, and placement into client dedicated pods.\n"
                    "• Partner with enterprise clients to create custom upskilling bootcamps."
                ),
                "requirements": (
                    "• 4+ years of professional software development experience.\n"
                    "• Passion for pedagogy, technical mentoring, and community building.\n"
                    "• Strong communication skills and empathy for aspiring engineers."
                ),
                "benefits": "Leadership role in African tech ecosystem, community impact, conference travel."
            }
        ]

        created_count = 0
        for pos in initial_positions:
            obj, created = JobPosition.objects.update_or_create(
                slug=pos["slug"],
                defaults=pos
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created_count} career openings (Total active: {JobPosition.objects.count()})."))
