from shop.models import *
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from tqdm import tqdm 
from colorama import Fore, Style, init  
init(autoreset=True)  

class Command(BaseCommand):
    help = 'Seed database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write(Fore.BLUE + 'Seeding database...')
        seed_categories()  
        seed_users()
        seed_sales()
        seed_products()
        seed_specifications()
        seed_product_photos()
        seed_product_categories()  
        self.stdout.write(Fore.BLUE + 'Database seeding completed.')

def seed_categories():
    Category.objects.all().delete()

    categories = [
        {"id": 1, "name": "computers.gaming", "description": "gaming"},
        {"id": 2, "name": "computers.learning", "description": "learning"},
        {"id": 3, "name": "computers.office", "description": "office"},
        {"id": 4, "name": "components.cases", "description": "cases"},
        {"id": 5, "name": "components.cooling", "description": "cooling"},
        {"id": 6, "name": "components.disks", "description": "disks"},
        {"id": 7, "name": "components.fans", "description": "fans"},
        {"id": 8, "name": "components.graphics", "description": "graphics"},
        {"id": 9, "name": "components.memoryRam", "description": "memoryRam"},
        {"id": 10, "name": "components.motherboards", "description": "motherboards"},
        {"id": 11, "name": "components.powerSupply", "description": "powerSupply"},
        {"id": 12, "name": "components.processors", "description": "processors"},
        {"id": 13, "name": "laptops.gaming", "description": "gaming"},
        {"id": 14, "name": "laptops.learning", "description": "learning"},
        {"id": 15, "name": "laptops.office", "description": "office"},
        {"id": 16, "name": "peripherals.mice", "description": "mice"},
        {"id": 17, "name": "peripherals.keyboards", "description": "keyboards"},
        {"id": 18, "name": "peripherals.monitors", "description": "monitors"},
        {"id": 19, "name": "networking.routers", "description": "routers"},
        {"id": 20, "name": "accessories.cables", "description": "cables"},
        {"id": 21, "name": "networking.networkCards", "description": "networkCards"},
        {"id": 22, "name": "peripherals.mousePads", "description": "mousePads"},
        {"id": 23, "name": "furniture.chairs", "description": "chairs"},
        {"id": 24, "name": "peripherals.headphones", "description": "headphones"},
        {"id": 25, "name": "furniture.desks", "description": "desks"},
        {"id": 26, "name": "mounts.mounts", "description": "mounts"},
        {"id": 27, "name": "peripherals.microphones", "description": "microphones"},
        {"id": 28, "name": "electronics.tablets", "description": "tablets"},
        {"id": 29, "name": "electronics.phones", "description": "phones"},
        {"id": 30, "name": "electronics.televisions", "description": "televisions"},
        {"id": 31, "name": "wearables.watches", "description": "watches"},
        {"id": 32, "name": "peripherals.printers", "description": "printers"},
        {"id": 33, "name": "peripherals.speakers", "description": "speakers"},
        {"id": 34, "name": "peripherals.webcams", "description": "webcams"},
        {"id": 35, "name": "accessories.powerBanks", "description": "powerBanks"},
        {"id": 36, "name": "peripherals.soundCards", "description": "soundCards"},
        {"id": 37, "name": "gaming.consoles", "description": "consoles"},
        {"id": 38, "name": "storage.usbFlashDrives", "description": "usbFlashDrives"},
    ]

    for category_data in tqdm(categories, desc="Seeding Categories", unit="category"):
        try:
            Category.objects.create(
                id=category_data["id"],
                name=category_data["name"],
                description=category_data["description"],
            )
            print(Fore.GREEN + f"Successfully added Category: {category_data['name']} (ID {category_data['id']})")
        except Exception as e:
            print(Fore.RED + f"Error seeding Category {category_data['name']} (ID {category_data['id']}): {e}")

    print(Fore.GREEN + "Categories successfully seeded.")

def seed_product_categories():
    ProductCategory.objects.all().delete()

    product_categories = [
        (1, 1), (2, 2), (3, 1), (4, 3), (5, 2), (6, 1), (7, 3), (8, 1), (9, 2), (10, 14),
        (11, 15), (12, 13), (13, 13), (14, 15), (15, 14), (16, 15), (17, 14), (18, 13), (19, 13), (20, 4),
        (21, 4), (22, 4), (23, 4), (24, 4), (25, 4), (26, 4), (27, 4), (28, 4), (29, 5), (30, 5),
        (31, 5), (32, 5), (33, 5), (34, 5), (35, 5), (36, 5), (37, 5), (38, 5), (39, 6), (40, 6),
        (41, 6), (42, 6), (43, 6), (44, 6), (45, 6), (46, 6), (47, 6), (48, 7), (49, 7), (50, 7),
        (51, 7), (52, 7), (53, 7), (54, 7), (55, 7), (56, 7), (57, 8), (58, 8), (59, 8), (60, 8),
        (61, 8), (62, 8), (63, 8), (64, 8), (65, 8), (66, 8), (67, 9), (68, 9), (69, 9), (70, 9),
        (71, 9), (72, 9), (73, 9), (74, 9), (75, 9), (76, 9), (77, 10), (78, 10), (79, 10), (80, 10),
        (81, 10), (82, 10), (83, 10), (84, 10), (85, 10), (86, 10), (87, 11), (88, 11), (89, 11), (90, 11),
        (91, 11), (92, 11), (93, 11), (94, 11), (95, 11), (96, 12), (97, 12), (98, 12), (99, 12), (100, 12),
        (101, 12), (102, 12), (103, 12), (104, 12), (105, 16), (106, 16), (107, 16), (108, 16), (109, 16), 
        (110, 16), (111, 16), (112, 16), (113, 16), (114, 16), (115, 16), (116, 17), (117, 17), (118, 17), (119, 17),
        (120, 17), (121, 17), (122, 17), (123, 17), (124, 17), (125, 17), (126, 18), (127, 18), (128, 18), (129, 18),
        (130, 18), (131, 18), (132, 18), (133, 18), (134, 18), (135, 18), (136, 19), (137, 19), (138, 19), (139, 19),
        (140, 19), (141, 19), (142, 19), (143, 19), (144, 19), (145, 19), (146, 20), (147, 20), (148, 20), (149, 20),
        (150, 20), (151, 20), (152, 20), (153, 20), (154, 20), (155, 20),
    ]

    for product_id, category_id in tqdm(product_categories, desc="Seeding ProductCategories", unit="relation"):
        try:
            product = Product.objects.get(id=product_id)
            category = Category.objects.get(id=category_id)
            ProductCategory.objects.create(product=product, category=category)
            print(Fore.GREEN + f"Successfully added relation: Product ID {product_id} -> Category ID {category_id}")
        except (Product.DoesNotExist, Category.DoesNotExist) as e:
            print(Fore.RED + f"Error seeding ProductCategory: {e}")
        except Exception as ex:
            print(Fore.RED + f"Unexpected error: {ex}")

    print(Fore.GREEN + "ProductCategory successfully seeded.")

def seed_sales():
    Sale.objects.all().delete()

    promotions = [
        {"id": 1, "discount_amount": 40.00, "start_date": "2024-04-18", "end_date": "2025-04-18"},
        {"id": 2, "discount_amount": 10.00, "start_date": "2024-04-19", "end_date": "2025-04-19"},
        {"id": 3, "discount_amount": 36.00, "start_date": "2024-04-20", "end_date": "2025-04-20"},
        {"id": 4, "discount_amount": 11.00, "start_date": "2024-04-21", "end_date": "2025-04-21"},
        {"id": 5, "discount_amount": 20.00, "start_date": "2024-04-22", "end_date": "2025-04-22"},
        {"id": 6, "discount_amount": 20.00, "start_date": "2024-04-23", "end_date": "2025-04-23"},
        {"id": 7, "discount_amount": 5.00, "start_date": "2024-04-24", "end_date": "2025-04-24"},
    ]

    for promotion in tqdm(promotions, desc="Seeding promotions", unit="promotion"):
            try:
                Sale.objects.create(
                    id=promotion["id"],
                    discount_amount=promotion["discount_amount"],
                    start_date=promotion["start_date"],
                    end_date=promotion["end_date"],
                )
                print(Fore.GREEN + f"Successfully added promotion ID {promotion['id']}.")
            except Exception as ex:
                print(Fore.RED + f"Error adding promotion ID {promotion['id']}: {ex}")

    print(Fore.GREEN + "Sales successfully seeded.")

def seed_users():
    User.objects.all().delete()

    users = [
        {"username": f"admin{i}", "email": f"admin{i}@example.com", "role": "admin", "password": "Admin123!"}
        for i in range(1, 6)
    ] + [
        {"username": f"client{i}", "email": f"client{i}@example.com", "role": "client", "password": "Client123!"}
        for i in range(1, 16)
    ]

    for user_data in tqdm(users, desc="Seeding users", unit="user"):
        try:
            validate_password(user_data["password"])

            User.objects.create(
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"],
                password=make_password(user_data["password"])  
            )
            print(Fore.GREEN + f"Successfully added user {user_data['username']}.")
        except ValidationError as e:
            print(Fore.RED + f"Validation error for user {user_data['username']}: {e}")
        except Exception as ex:
            print(Fore.RED + f"Error adding user {user_data['username']}: {ex}")

    print(Fore.GREEN + "Users successfully seeded.")

def seed_products():
    Product.objects.all().delete()

    products = [
        {
            "id": 1,
            "name": "Set Z1 | Ryzen 7500F, RTX 4060 8GB, 16GB DDR5, 500GB SSD, 650W, Aramis Midi ARGB",
            "price": 910.0,
            "old_price": 950.0,
            "description": """<h3>Ready-Made Gaming PC Set</h3>
                <p>Choosing a ready-made computer set is an ideal solution for those who prefer not to risk selecting components themselves or assembling them into a functioning unit. However, many off-the-shelf products can be traps for inexperienced users, lured by attractive prices but unaware of potential quality issues or outdated components.</p>
                <p>As gamers ourselves with over a decade of experience, weve completed hundreds, if not thousands, of set orders. This allows us to expertly select components and configure the system so that the computer delivered to you only requires pressing the POWER button to start enjoying virtual gameplay.</p>
                <p>With your purchased set, we perform several activities for you. We install the operating system (unactivated Windows 10), all necessary drivers, and make essential updates, including BIOS updates for enhanced security and performance. Depending on the components chosen, we also perform overclocking to safely boost performance in games and applications.</p>
                <p>You can rest assured about transport. The ordered set will be delivered by an insured courier, with the computers interior protected to prevent mechanical damage to the components even in case of accidental drops. These protections must be removed before the first startup.</p>
                <p>We provide a Door-to-Door warranty for the purchased set, meaning that in the event of a component failure, well collect the defective part or the entire computer from you and service it according to the manufacturers warranty terms.</p>
                """,
            "sale_id": 1,
        },
        {
            "id": 2,
            "name": "Set Z2 | Ryzen 5 5600, RTX 4060 8GB, 16GB DDR4, 1TB SSD, Signum 300 ARGB, 750W",
            "price": 960.0,
            "old_price": 990.0,
            "description": """<h3>Ready-Made Computer Set: Your Gaming Solution</h3>
                <p>For those lacking expertise or the desire to select and assemble components, a ready-made computer set is the perfect solution. Unfortunately, off-the-shelf products can be a trap for the inexperienced, lured by attractive prices without realizing the potential drawbacks of poor quality or outdated components, hindering future expansion or modernization.</p>
                <p>As gamers with over a decade of experience, weve completed countless set orders, enabling us to expertly select components and configure systems. Your delivered computer only requires pressing the POWER button to start enjoying virtual gameplay.</p>
                <p>With your purchase, we go the extra mile! We install the operating system (unactivated Windows 10), all drivers, and necessary updates (including BIOS) to enhance security and speed. Depending on your components, we may even perform overclocking—safely boosting performance in games and applications through programmatic modification of processor, RAM, and graphics card parameters.</p>
                <p>Transport concerns are unnecessary. Your ordered set will be sent via insured courier, with the computers interior protected to prevent mechanical damage, even in case of drops. These protections must be removed before the first start-up.</p>
                <p>We offer a Door-to-Door warranty, ensuring peace of mind. In the event of a component failure, we collect the defective part or the entire computer and service it according to the manufacturers warranty terms.</p>
                """,
            "sale_id": None,
        },
        {
            "id": 3,
            "name": "Set Z3 | Intel I7-14700KF, RTX 4070 Ti SUPER 16GB, 32GB DDR5, 1TB SSD, 750W, ARX 500 ARGB",
            "price": 1975.0,
            "old_price": 2225.0,
            "description": """<h3>Ready-Made Computer Sets: Your Hassle-Free Solution</h3>
                <p>For those lacking technical expertise or the desire to navigate component selection and assembly, ready-made computer sets offer an ideal solution. However, its crucial to avoid falling into the trap of attractive prices that may disguise poor quality or outdated components, hindering future expansion or modernization.</p>
                <p>As avid gamers ourselves, boasting over a decade of experience and having completed hundreds, if not thousands, of set orders, we possess the expertise to meticulously select components and perform full configuration. Our goal is to deliver a computer that only requires pressing the POWER button on the casing, allowing you to dive straight into virtual gameplay.</p>
                <p>With your purchased set, we go above and beyond! We not only install the operating system (unactivated Windows 10) but also all necessary drivers and updates, including BIOS updates that enhance security and speed. Depending on your chosen components, we may even perform overclocking, safely boosting performance in games and applications through programmatic modification of processor, RAM, and graphics card parameters.</p>
                <p>Transportation worries are a thing of the past. Your ordered set will be securely sent to you by insured courier, with the interior of the computer meticulously protected to prevent mechanical damage, even in the event of mishaps during transit. These protections must be removed before the first start-up.</p>
                <p>Rest assured with our Door-to-Door warranty for the purchased set. In the unfortunate event of a component failure, well collect the defective component or the entire computer from you and service it in accordance with the warranty terms of the manufacturer.</p>
            """,
            "sale_id": None,
        },
        {
            "id": 4,
            "name": "Set Z4 | Ryzen 7 5700X, RTX 4060 8GB, 16GB DDR4, 500GB SSD, Aramis ARGB, 550W",
            "price": 1630.0,
            "old_price": 1680.0,
            "description": """<h3>Why Choose a Ready-Made Computer Set?</h3>
                <p>For those lacking the technical know-how or the desire to navigate the complexities of selecting and assembling components, a ready-made computer set offers an ideal solution. However, its important to beware of the pitfalls associated with ready-made products, which can often entice inexperienced users with attractive prices, only to deliver poor-quality or outdated components, hindering future expansion or modernization.</p>
                <h3>Our Expertise, Your Confidence</h3>
                <p>As avid gamers ourselves with over a decade of experience and countless orders fulfilled, we possess the expertise to meticulously select components and perform full configurations. Our goal is to deliver a computer thats ready to use upon delivery—all you need to do is press the POWER button and dive into your virtual adventures.</p>
                <h3>Comprehensive Service</h3>
                <p>With your purchased set, we go the extra mile. We not only install the operating system (unactivated Windows 10) but also ensure that all drivers and necessary updates, including BIOS updates, are installed to enhance the security and speed of your computer. Depending on your chosen components, we may even perform overclocking, safely boosting performance in games and applications through programmatic modification of processor, RAM, and graphics card parameters.</p>
                <h3>Worry-Free Transport</h3>
                <p>Forget about transportation concerns. Your ordered set will be securely sent to you by insured courier, with meticulous protection ensuring that even if the shipment is dropped, there will be no mechanical damage to the components. Please remember to remove these protections before the first start-up.</p>
                <h3>Peace of Mind Warranty</h3>
                <p>With our Door-to-Door warranty, you can rest assured that in the event of a component failure, well take care of everything. Whether its collecting the defective component or the entire computer from you, well ensure that its serviced in accordance with the warranty terms of the manufacturer, providing you with peace of mind and uninterrupted gaming enjoyment.</p>""",
            "sale_id": None,
        },
        {
            "id": 5,
            "name": "Set Z5 | Intel I5-14400F, RX 7800 XT 12GB, 16GB DDR4, 500GB SSD, 650W, MSI 112 ARGB",
            "price": 261.0,
            "old_price": 311.0,
            "description": """<h3>Why Choose a Ready-Made Computer Set?</h3>
                <p>For individuals lacking technical expertise or the desire to select and assemble components, a ready-made computer set offers an ideal solution. However, ready-made products can often be a double-edged sword, particularly for inexperienced users. They may be lured by attractive prices but unknowingly receive components of poor quality or outdated technology, limiting future expansion or upgrades.</p>
                <h3>Our Expertise, Your Peace of Mind</h3>
                <p>As avid gamers ourselves with over a decade of experience, having fulfilled hundreds, if not thousands, of orders, we are well-equipped to select components and perform full configurations. This ensures that the computer delivered to you requires nothing more than pressing the POWER button to enjoy seamless virtual gameplay.</p>
                <h3>Comprehensive Service</h3>
                <p>With your purchased set, we go above and beyond. We not only install the operating system (unactivated Windows 10) but also ensure that all drivers and necessary updates, including BIOS updates, are installed to enhance the security and speed of your computer. Depending on your chosen components, we may even perform overclocking—safely boosting performance in games and applications by programmatically modifying the parameters of the processor, RAM, and graphics card.</p>
                <h3>Worry-Free Transport</h3>
                <p>Forget about transportation worries. Your ordered set will be securely sent to you by insured courier. The interior of the computer is meticulously protected during transport, ensuring that even if the shipment is dropped, there will be no mechanical damage to the components. Remember to remove these protections before the first start-up.</p>
                <h3>Peace of Mind Warranty</h3>
                <p>With our Door-to-Door warranty, you can rest assured that in the event of a component failure, weve got you covered. Whether its collecting the defective component or the entire computer from you, well service it in accordance with the warranty terms of the manufacturer, ensuring minimal disruption to your gaming experience.</p>""",
            "sale_id": None,
        },
        {
            "id": 6,
            "name": "Set Z6 | Intel I5-14600KF, RX 7900 GRE 16GB, 16GB DDR5, 500GB SSD, 700W, ARX 500 ARGB",
            "price": 732.0,
            "old_price": 650.0,
            "description": """<h3>Why Choose a Ready-Made Computer Set?</h2>
                <p>For individuals lacking technical expertise or the desire to select and assemble components themselves, a ready-made computer set offers an ideal solution. However, its important to be cautious, as ready-made products can sometimes lead to disappointment for inexperienced users. They may be attracted by low prices but unknowingly receive components of poor quality or outdated technology, hindering future expansion or upgrades.</p>
                <h3>Our Experience, Your Confidence</h2>
                <p>As gamers ourselves with over 10 years of experience and having fulfilled hundreds, if not thousands, of orders for sets, we have the expertise to select components and perform full configurations. This ensures that the computer delivered to you only requires pressing the POWER button on the casing to enjoy seamless virtual gameplay.</p>
                <h3>Comprehensive Services Included</h2>
                <p>With your purchased set, we go the extra mile. We not only install the operating system (unactivated Windows 10) but also all necessary drivers and updates, including BIOS updates, to enhance the security and speed of your computer. Depending on the selected components, we may even perform overclocking—safely boosting performance in games and applications by programmatically modifying the parameters of the processor, RAM, and graphics card.</p>
                <h3>Worry-Free Transport</h2>
                <p>Forget about transport concerns. Your ordered set will be securely sent to you by insured courier. The interior of the computer is meticulously protected during transport, ensuring that even if the shipment is dropped, there will be no mechanical damage to the components. Remember to remove these protections before the first start-up.</p>
                <h3>Peace of Mind Warranty</h2>
                <p>With our Door-to-Door warranty, you can rest assured that in the event of a component failure, weve got you covered. Whether its collecting the defective component or the entire computer from you, well service it in accordance with the warranty terms of the manufacturer, ensuring minimal disruption to your gaming experience.</p>""",
            "sale_id": None,
        },
        {
            "id": 7,
            "name": "Set Z7 | Ryzen 5 7600, RX 7800 XT 16GB, 16GB DDR5, 500GB SSD, 112R ARGB, 700W",
            "price": 650.0,
            "old_price": 725.0,
            "description": """<h3>Why Choose a Ready-Made Computer Set?</h3>
                <p>A ready-made computer set offers an ideal solution for individuals who lack the expertise or desire to select and assemble components themselves. However, ready-made products can sometimes lead to disappointment for inexperienced users. They may be enticed by attractive prices but overlook the fact that some components are of poor quality or outdated, limiting future expansion or upgrades.</p>
                <h3>Expertise and Experience</h3>
                <p>As gamers ourselves with over 10 years of experience, we have completed hundreds, if not thousands, of orders for sets. This allows us to properly select components and perform full configurations, ensuring that the computer delivered to you requires only pressing the POWER button on the casing to enjoy seamless virtual gameplay.</p>
                <h3>Comprehensive Services Included</h3>
                <p>With your purchased set, we go above and beyond. We not only install the operating system (unactivated Windows 10) but also all necessary drivers and updates, including BIOS updates, to enhance the security and speed of your computer. Depending on the selected components, we may even perform overclocking—safely boosting performance in games and applications by modifying the parameters of the processor, RAM, and graphics card.</p>
                <h3>Worry-Free Transport</h3>
                <p>Forget transport concerns. Your ordered set will be securely sent to you by insured courier. The interior of the computer is meticulously protected during transport, ensuring that even if the shipment is dropped, there will be no mechanical damage to the components. Remember to remove these protections before the first start-up.</p>
                <h3>Peace of Mind Warranty</h3>
                <p>With our Door-to-Door warranty, you can rest assured that in the event of a component failure, we have you covered. Whether its collecting the defective component or the entire computer from you, well service it in accordance with the warranty terms of the manufacturer, ensuring minimal disruption to your gaming experience.</p>""",
            "sale_id": None,
        },
        {
            "id": 8,
            "name": "Set Z8 | Ryzen 7 7800X3D, RX 7900 XTX 24GB, 32GB DDR5, 2TB SSD, Regnum 400 ARGB, 1000W",
            "price": 420.0,
            "old_price": 510.0,
            "description": """<h3>Why Choose a Ready-Made Computer Set?</h3>
                <p>A ready-made computer set is an ideal solution for individuals who lack the necessary knowledge or expertise to select and assemble components themselves. While the allure of attractive prices may be tempting, ready-made products can often be a trap for inexperienced users. They may unknowingly purchase components of poor quality or outdated technology, hindering future expansion or modernization of their machine.</p>
                <h3>Expertise and Experience</h3>
                <p>As avid gamers ourselves with over a decade of experience, we have completed hundreds, if not thousands, of orders for computer sets. This extensive experience allows us to expertly select components and perform full configurations. When you receive your computer, it will be ready to use with just the press of the POWER button, allowing you to immediately enjoy virtual gameplay.</p>
                <h3>Comprehensive Services Included</h3>
                <p>When you purchase a set from us, we go the extra mile for you. In addition to installing the operating system (unactivated Windows 10), we also install all necessary drivers and perform essential updates, including BIOS updates, to enhance the security and speed of your computer. Depending on the components selected, we may even perform overclocking to safely boost performance in games and applications by modifying processor, RAM, and graphics card parameters.</p>
                <h3>Worry-Free Transport</h3>
                <p>Rest assured, you dont need to worry about transport logistics. Your ordered set will be securely delivered to you by an insured courier. The interior of the computer is carefully protected during transport to prevent mechanical damage to components, even in the event of a drop. Remember to remove these protections before starting up your computer for the first time.</p>
                <h3>Peace of Mind Warranty</h3>
                <p>With our Door-to-Door warranty, you can have peace of mind knowing that in the event of a component failure, we have you covered. Whether its collecting the defective component or the entire computer from you, we will service it in accordance with the warranty terms of the manufacturer, ensuring minimal disruption to your gaming experience.</p>""",
            "sale_id": None,
        },
        {
            "id": 9,
            "name": "Set Z9 | G4M3R HERO i7-13700F/32GB/1TB/RTX4060Ti/W11x",
            "price": 3900.0,
            "old_price": 4200.0,
            "description": """<h3>Choose Smart: Dawid Olko's Opinion</h3>
                <p>Thinking about buying a computer? Not sure how the G4M3R Hero (2023) will perform in everyday use? Read the opinion of Piotr Smoła, editor of the Geex portal.</p>""",
            "sale_id": None,
        },
        {
            "id": 10,
            "name": "Apple MacBook Air M2/16GB/256/Mac OS Midnight",
            "price": 4900.0,
            "old_price": 5200.0,
            "description": """<h3>Apple MacBook Air M2/16GB/256/Mac OS Midnight</h3>
                <p>Discover the epitome of elegance and performance with the Apple MacBook Air M2. Combining cutting-edge technology with sleek design, this laptop redefines portability and productivity.</p>
                <p>Powered by the innovative M2 chip, this MacBook Air delivers lightning-fast performance and remarkable efficiency, ensuring smooth multitasking and seamless user experience. With 16GB of RAM, it effortlessly handles demanding tasks, from creative projects to productivity workflows.</p>
                <p>The spacious 256GB SSD provides ample storage for your files, documents, and multimedia content, while ensuring swift data access and fast boot-up times.</p>
                <p>Featuring macOS Midnight, Apples intuitive and powerful operating system, the MacBook Air offers a seamless and secure computing environment. Enjoy a wide range of built-in apps, robust security features, and seamless integration with other Apple devices.</p>
                <p>Experience stunning visuals and vibrant colors on the high-resolution display, ideal for immersive multimedia consumption, content creation, and professional tasks.</p>
                <p>Whether youre a creative professional, a student, or a business user, the Apple MacBook Air M2/16GB/256/Mac OS Midnight is the perfect companion for all your computing needs, combining power, style, and versatility in a compact and lightweight package.</p>""",
            "sale_id": None,
        },
            {
            "id": 11,
            "name": "HP 255 G9 Ryzen 5-5625U/16GB/512/Win11",
            "price": 1578.0,
            "old_price": 1536.0,
            "description": """<h3>HP 255 G9 Ryzen 5-5625U/16GB/512/Win11</h3>
                <p>Experience seamless performance and reliable computing with the HP 255 G9 laptop. Powered by the efficient Ryzen 5-5625U processor, this laptop offers impressive speed and responsiveness for both work and entertainment.</p>
                <p>With 16GB of RAM, multitasking becomes effortless, allowing you to run multiple applications simultaneously without any slowdowns. The spacious 512GB SSD provides ample storage space for your files, documents, and multimedia content while ensuring fast data access and quick boot-up times.</p>
                <p>Equipped with Windows 11, the latest operating system from Microsoft, the HP 255 G9 offers a modern and intuitive computing experience. Enjoy enhanced security features, improved multitasking capabilities, and a sleek user interface designed to maximize productivity.</p>
                <p>The HP 255 G9 boasts a sleek and durable design, making it perfect for both office use and on-the-go computing. Its lightweight construction and long battery life ensure that you can stay productive wherever you go.</p>
                <p>Whether youre working on spreadsheets, streaming HD videos, or browsing the web, the HP 255 G9 Ryzen 5-5625U/16GB/512/Win11 laptop delivers reliable performance and versatility for all your computing needs.</p>""",
            "sale_id": None,
        },
        {
            "id": 12,
            "name": "MSI Thin GF63 i5-12450H/16GB/512 RTX2050 144Hz",
            "price": 1294.0,
            "old_price": 1242.0,
            "description": """<h3>MSI Thin GF63 i5-12450H/16GB/512 RTX2050 144Hz</h3>
                <p>Unleash the power of portable gaming with the MSI Thin GF63 laptop. Featuring the latest Intel Core i5-12450H processor, this laptop delivers exceptional performance for gaming, content creation, and multitasking.</p>
                <p>Equipped with 16GB of DDR4 RAM, the MSI Thin GF63 ensures smooth and responsive performance, allowing you to run multiple applications simultaneously without any lag. The 512GB SSD provides ample storage space for your games, media files, and software, while offering lightning-fast data transfer speeds.</p>
                <p>Experience immersive gaming visuals with the NVIDIA GeForce RTX 2050 graphics card. With its powerful GPU and dedicated video memory, you can enjoy smooth gameplay and stunning graphics on the laptops vibrant 144Hz display.</p>
                <p>The MSI Thin GF63 features a sleek and lightweight design, making it perfect for gaming on the go. Its thin bezels and slim profile enhance the overall aesthetics, while the durable construction ensures long-lasting durability.</p>
                <p>Stay connected and productive with a range of ports, including USB Type-C, HDMI, and more. The laptop also features Wi-Fi 6 support for faster wireless connectivity and Bluetooth compatibility for seamless device pairing.</p>
                <p>Whether youre gaming, working, or streaming content, the MSI Thin GF63 i5-12450H/16GB/512 RTX2050 144Hz laptop offers powerful performance and portability for all your computing needs.</p>""",
            "sale_id": None,
        },
        {
            "id": 13,
            "name": "ASUS Vivobook 15 i5-1235U/16GB/512/Win11",
            "price": 654.0,
            "old_price": 665.0,
            "description": """<h3>ASUS Vivobook 15 i5-1235U/16GB/512/Win11</h3>
                <p>Experience productivity and style with the ASUS Vivobook 15, featuring powerful performance in a sleek and portable design. Powered by the Intel Core i5-1235U processor and equipped with 16GB of RAM, this laptop delivers smooth multitasking and responsiveness for everyday computing tasks.</p>
                <p>With its 15.6-inch Full HD display, the ASUS Vivobook 15 offers vibrant visuals and crisp details, whether youre working on documents, streaming content, or browsing the web. The slim bezel design maximizes screen space, providing an immersive viewing experience without adding bulk to the laptop.</p>
                <p>Featuring a spacious 512GB SSD, this laptop offers ample storage for your files, software, and multimedia content, while ensuring fast boot times and quick access to your data. With Windows 11 pre-installed, youll enjoy the latest features and enhancements for productivity and creativity.</p>
                <p>The ASUS Vivobook 15 combines performance with portability, making it ideal for on-the-go professionals and students. Its lightweight and compact design allow you to take it anywhere, whether youre commuting to work or studying in a coffee shop.</p>
                <p>Equipped with a full range of connectivity options, including USB Type-C, USB 3.2, HDMI, and Wi-Fi 6, the ASUS Vivobook 15 offers seamless connectivity to peripherals, displays, and networks. Stay productive and connected wherever you go with this versatile and reliable laptop.</p>
                <p>Whether youre tackling everyday tasks or working on creative projects, the ASUS Vivobook 15 provides the performance and versatility you need to get things done. With its sleek design, powerful hardware, and convenient features, its the perfect companion for work and play.</p>""",
            "sale_id": None,
        },
        {
            "id": 14,
            "name": "Dell Inspiron 3520 i5-1235U/16GB/1TB/Win11 120Hz",
            "price": 1500.0,
            "old_price": 1550.0,
            "description": """<h3>Dell Inspiron 3520 i5-1235U/16GB/1TB/Win11 120Hz</h3>
                <p>Experience superior performance and immersive visuals with the Dell Inspiron 3520. Powered by the Intel Core i5-1235U processor and equipped with 16GB of RAM, this laptop delivers blazing-fast speeds and smooth multitasking for enhanced productivity.</p>
                <p>The Dell Inspiron 3520 features a stunning 120Hz display, offering buttery-smooth visuals and ultra-responsive gameplay. Whether youre editing videos, playing games, or watching movies, the high refresh rate ensures a seamless viewing experience with minimal motion blur.</p>
                <p>With a spacious 1TB hard drive, this laptop provides ample storage for your files, documents, and multimedia content. Store your entire digital library without worrying about running out of space, and enjoy fast access to your data for improved workflow efficiency.</p>
                <p>Pre-installed with Windows 11, the Dell Inspiron 3520 offers the latest features and enhancements for enhanced productivity and creativity. Navigate the user-friendly interface, access your favorite apps with ease, and enjoy seamless integration with Microsoft services.</p>
                <p>Designed for performance and portability, the Dell Inspiron 3520 features a sleek and lightweight design thats perfect for on-the-go professionals and students. Take it with you wherever you go and stay productive, whether youre working from home, at the office, or on the go.</p>
                <p>Equipped with a range of connectivity options, including USB Type-C, USB 3.2, HDMI, and Wi-Fi 6, the Dell Inspiron 3520 offers seamless connectivity to peripherals, displays, and networks. Stay connected and productive wherever you are with reliable and high-speed connections.</p>
                <p>Whether youre tackling demanding work tasks or enjoying multimedia entertainment, the Dell Inspiron 3520 delivers the performance and versatility you need to stay productive and entertained. With its powerful hardware, immersive display, and convenient features, its the perfect laptop for work and play.</p>""",
            "sale_id": None,
        },
        {
            "id": 15,
            "name": "Dell Inspiron 3520 i5-1235U/16GB/1TB/Win11 120Hz Srebrny",
            "price": 920.0,
            "old_price": 930.0,
            "description": """<h3>Dell Inspiron 3520 i5-1235U/16GB/1TB/Win11 120Hz Silver</h3>
                <p>Dell Inspiron 3520 is a great laptop that combines performance, elegance and functionality. Equipped with an Intel Core i5-1235U processor and 16GB RAM, it provides incredible speed and smooth switching between applications so that you can effectively perform your daily tasks.</p>
                <p>The Dell Inspiron 3520 Silver laptop is distinguished by its elegant appearance and solid construction, which makes it perfect for both work and relaxation. The matte surface of the casing provides resistance to dirt and scratches, and subtle details give it a unique look.</p>
                <p>Equipped with a screen with a refresh rate of 120Hz, the Dell Inspiron 3520 Silver laptop provides a smooth and responsive visual experience when watching movies, browsing the web or playing games. The image is clear and the movements are smooth, allowing you to fully enjoy every moment of use.</p>
                <p>Thanks to the 1TB hard drive capacity, you have enough space to store your files, documents and multimedia. Regardless of whether you have a large collection of photos, movies or music, you will always have quick access to your data, which will allow you to effectively manage your resources.</p>
                <p>The pre-installed Windows 11 system provides convenient and intuitive operation of the Dell Inspiron 3520 laptop. Thanks to the latest features and system improvements, you can effectively perform your tasks, use your favorite applications and enjoy smooth work every day.</p>
                <p>The Dell Inspiron 3520 Silver laptop offers a wide range of features and capabilities, thanks to which you can be more productive and creative in work, study or entertainment. You can easily connect to various devices and networks, thanks to a variety of ports and wireless technologies.</p>
                <p>Whether you need a laptop for work, study or entertainment, the Dell Inspiron 3520 Silver will meet your expectations in terms of performance, functionality and design. With a solid construction, elegant appearance and advanced features, it is an ideal solution for those looking for a versatile and reliable laptop.</p>""",
            "sale_id": 2,
        },
        {
            "id": 16,
            "name": "Acer Chromebook 315 N4500/8GB/128/FHD ChromeOS",
            "price": 556.0,
            "old_price": 578.0,
            "description": """<h3>Acer Chromebook 315 N4500/8GB/128/FHD ChromeOS</h3>
                <p>Acer Chromebook 315 is a powerful laptop that provides reliability, speed and a great user experience. Equipped with an Intel N4500 processor and 8GB of RAM, this laptop provides smooth operation and fast application loading, making everyday tasks easier.</p>
                <p>Thanks to the ChromeOS system, the Acer Chromebook 315 offers convenient and intuitive operation and access to a wide range of applications available in the Google Play store. So you can freely use your favorite applications for work, study or entertainment, knowing that they will work efficiently and without problems.</p>
                <p>The Acer Chromebook 315 laptop is equipped with a Full HD screen that provides a clear and sharp image. Thanks to this, you can enjoy high visual quality while browsing websites, watching movies or using multimedia applications.</p>
                <p>With a large capacity of 128GB SSD, you have enough space to store your files, documents and multimedia. Additionally, using cloud services, you can access your data from any location and device, which provides flexibility and mobility at work.</p>
                <p>The durable battery of the Acer Chromebook 315 laptop provides long hours of work without the need for frequent charging. Thanks to this, you can work calmly all day long without worrying about losing power, which increases your productivity and mobility.</p>
                <p>The Acer Chromebook 315 laptop is also a lightweight and compact design, which makes it easy to take with you on a trip or to a meeting. The materials used are durable and resistant to damage, ensuring long-lasting performance and reliability.</p>
                <p>To sum up, the Acer Chromebook 315 N4500/8GB/128/FHD ChromeOS is an excellent choice for those looking for an efficient, reliable and easy-to-use laptop for work, study or entertainment. With advanced features, convenient operation and attractive design, it will meet the expectations of even the most demanding users.</p>""",
            "sale_id": None,
        },
        {
            "id": 17,
            "name": "Lenovo Yoga Slim 6-14 i5-1240P/16GB/512/Win11",
            "price": 850.0,
            "old_price": 855.0,
            "description": """<h3>Lenovo Yoga Slim 6-14 i5-1240P/16GB/512/Win11</h3>
                <p>The Lenovo Yoga Slim 6-14 is a stylish and efficient laptop that provides excellent performance, mobility and functionality. Equipped with an Intel i5-1240P processor and 16GB of RAM, this laptop provides smooth operation and fast application loading, making it easier to both work and play.</p>
                <p>Thanks to Windows 11, the Lenovo Yoga Slim 6-14 offers a modern interface, intuitive operation and access to a wide range of applications available in the Microsoft Store. So you can freely use your favorite programs and tools, knowing that they will work efficiently and without problems.</p>
                <p>The Lenovo Yoga Slim 6-14 laptop is equipped with a Full HD display that provides a clear and sharp image. Thanks to IPS technology, colors are natural and faithfully reproduced, which makes watching movies, browsing photos or using multimedia applications a real pleasure.</p>
                <p>With a large capacity of the 512GB SSD drive, you have enough space to store your files, documents and multimedia. Additionally, using cloud services, you can access your data from anywhere and on any device, which provides flexibility and mobility at work.</p>
                <p>The durable battery of the Lenovo Yoga Slim 6-14 laptop provides long hours of work without the need for frequent charging. Thanks to this, you can work calmly all day long without worrying about losing power, which increases your productivity and mobility.</p>
                <p>The Lenovo Yoga Slim 6-14 laptop is also a lightweight and compact design, which makes it easy to take with you on a trip or to a meeting. The materials used are durable and resistant to damage, ensuring long-lasting performance and reliability of use.</p>
                <p>To sum up, the Lenovo Yoga Slim 6-14 i5-1240P/16GB/512/Win11 is an excellent choice for those looking for an elegant, efficient and reliable laptop for work, study or entertainment. Thanks to advanced features, convenient operation and attractive design, it will meet the expectations of even the most demanding users.</p>""",
            "sale_id": None,
        },
        {
            "id": 18,
            "name": "Microsoft Surface Laptop Studio I7/32GB/2TB/GeForce",
            "price": 3900.0,
            "old_price": 4200.0,
            "description": """<h3>Microsoft Surface Laptop Studio I7/32GB/2TB/GeForce</h3>
                <p>Microsoft Surface Laptop Studio is a revolutionary laptop that combines extraordinary performance, versatility, and innovative design. Equipped with a powerful Intel Core i7 processor, 32GB RAM, and a 2TB SSD drive, this laptop provides unmatched computing power and huge storage space.</p>
                <p>Thanks to the dedicated GeForce graphics card, Microsoft Surface Laptop Studio enables smooth and responsive operation of even the most demanding applications and games. The PixelSense display with 4K resolution allows you to enjoy incredible sharpness, color depth, and excellent image quality, which makes every task a real pleasure.</p>
                <p>The modern design of Microsoft Surface Laptop Studio is characterized by a unique design that allows for a smooth change of work mode - from a traditional laptop to a creative workstation. Thanks to the intuitive screen lifting mechanism, you can adjust the laptop to your needs and work comfortably in any position.</p>
                <p>The Microsoft Surface Laptop Studio laptop has been designed with maximum comfort and mobility in mind. Its weight and compact dimensions mean you can take it with you anywhere, regardless of whether you work in the office, travel or work remotely.</p>
                <p>The durable battery provides long hours of work without having to charge, allowing for complete freedom of action and productivity throughout the day. Additionally, the integrated Windows 11 system provides convenience of use, modern functions and access to a wide range of applications available in the Microsoft Store.</p>
                <p>To sum up, the Microsoft Surface Laptop Studio I7/32GB/2TB/GeForce is not only an elegant and efficient laptop, but also a versatile creative station that allows you to express your creativity in any situation. Thanks to advanced functions, innovative design and unparalleled build quality, it will meet the expectations of even the most demanding users.</p>""",
            "sale_id": None,
        },
        {
            "id": 19,
            "name": "Microsoft Surface Laptop Studio 2 i7/32GB/1TB/GeForce RTX4050",
            "price": 4900.0,
            "old_price": 5200.0,
            "description": """<h3>Microsoft Surface Laptop Studio 2 i7/32GB/1TB/GeForce RTX4050</h3>
                <p>Microsoft Surface Laptop Studio 2 is the latest iteration of an innovative laptop that combines elegance, performance and versatility. Equipped with a powerful Intel Core i7 processor, 32GB of RAM and a fast 1TB SSD, this laptop provides unparalleled computing power and a huge amount of storage space.</p>
                <p>With a dedicated GeForce RTX4050 graphics card, Microsoft Surface Laptop Studio 2 offers unparalleled graphic capabilities, ensuring smooth and responsive operation of even the most demanding applications and games. The 4K PixelSense display provides incredible image quality, excellent sharpness and wide viewing angles, making every job a real pleasure.</p>
                <p>The innovative design of Microsoft Surface Laptop Studio 2 allows for a smooth change of work mode - from a traditional laptop to a creative workstation. Thanks to the intuitive screen lifting mechanism, you can adjust the laptop to your needs and work comfortably in any position.</p>
                <p>The Microsoft Surface Laptop Studio 2 laptop has been designed with maximum comfort and mobility in mind. Thanks to its lightness and compact dimensions, you can take it with you anywhere, regardless of whether you work in the office, travel or work remotely.</p>
                <p>The durable battery provides long hours of work without having to charge, allowing for complete freedom of operation throughout the day. Additionally, the integrated Windows 11 system provides convenience of use, modern functions and access to a wide range of applications available in the Microsoft Store.</p>
                <p>To sum up, the Microsoft Surface Laptop Studio 2 i7/32GB/1TB/GeForce RTX4050 is not only an elegant and efficient laptop, but also a versatile creative station that allows you to express your creativity in any situation. Thanks to advanced functions, innovative design and unparalleled build quality, it will meet the expectations of even the most demanding users.</p>""",
            "sale_id": None,
        },
        {
            "id": 20,
            "name": "Fury Shobo SH4F RGB",
            "price": 84.0,
            "old_price": 100.0,
            "description": """<h3>Fury Shobo SH4F RGB Black computer case</h3>
                    <p>Check out <strong>Fury Shobo SH4F RGB</strong> - a clever computer case with efficient cooling and RGB backlighting. Compatible with ATX motherboards and water cooling systems (AIO 360/280/240/140/120), Shobo SH4F RGB includes as many as 4 RGB fans, a mesh front and dust protection.</p>
                    <p>The futuristic, geometric shape will appeal to both hardcore gamers and supporters of a more subdued design. The left side panel made of tempered glass allows you to display the inside of the case and the powerful components hidden inside - also with RGB, especially since the installed fans are factory-illuminated.</p>
                    <h4>Low temperatures, high efficiency</h4>
                    <p>Thanks to 4 efficient 120 mm RGB fans (one at the back, three at the front) and an open top and mesh front, Shobo SH4F RGB ensures free air flow through the housing. Combined with the possibility of installing an air CPU cooler up to 161 mm and a total of 8 fans (3 × front, 2 × top, 1 × rear, 2 × bottom), we get efficient cooling that can handle really powerful components.</p>
                    <h4>High cooling</h4>
                    <p>Do you want to expand your fragging machine with efficient water cooling? With Fury Shobo SH4F RGB its childs play. The housing allows you to install AIO LC coolers with the following sizes: front (360/280/240/140/120 mm), top (240/120 mm) and rear (120 mm). Such wide compatibility means freedom in selecting components - even the most powerful ones that require really high-end cooling.</p>
                    <h4>Effective dust barrier</h4>
                    <p>Dust penetrating the interior of the case is the nightmare of every computer system. With Fury Shobo SH4F RGB you dont have to worry about that anymore. The housing is completely filtered against dust: from the top and bottom, and the "mesh" front has very dense meshes with a diameter clearly below 1 mm, providing protection against dirt and facilitating free air flow.</p>
                    <h4>Great possibilities in a small housing</h4>
                    <p>While maintaining small external dimensions, the Shobo SH4F RGB case offers full compatibility with ATX, micro-ATX and mini-ITX motherboards. You can fit in it a powerful graphics card up to 330 mm long, up to 3 drives/media (HDD/SSD) and a CPU air cooler up to 161 mm. Two-chamber design with a "basement" for the power supply and numerous cable entries mean no mess and easy organization of components.</p>""",
            "sale_id": None,
        },
            {
            "id": 21,
            "name": "Fury Shobo SH4F Tempered Glass",
            "price": 64.0,
            "old_price": 100.0,
            "description": """<h3>SHOBO SH4F GAMING HOUSING – ENCASE YOUR FURY</h3>
                <p>Get your hands on Fury Shobo SH4F - a smart computer case with efficient cooling. Compatible with ATX motherboards and water cooling systems (AIO 360/280/240/140/120), Shobo SH4F has as many as 4 efficient PWM fans, a mesh front and dust protection. Welcome to a world of exciting possibilities and low temperatures!</p>
                <h3>LOW TEMPERATURES, HIGH EFFICIENCY</h3>
                <p>Build a beast, not a computer! Thanks to 4 efficient 120 mm PWM fans (one at the back, three at the front) and an open top and mesh front, Shobo SH4F ensures free air flow through the case. Combined with the possibility of installing an air CPU cooler up to 161 mm and a total of 8 fans (3 × front, 2 × top, 1 × rear, 2 × bottom), we get efficient cooling that can cope with really powerful components. Fans of extreme performance can also count on compatibility with integrated AIO LC liquid cooling systems.</p>
                <h3>TAKE COOLING TO THE NEXT LEVEL</h3>
                <p>Do you want to expand your fragging machine with efficient water cooling? With Fury Shobo SH4F its childs play! The housing allows you to install AIO LC coolers with the following sizes: front (360/280/240/140/120 mm), top (240/120 mm) and rear (120 mm). Such wide compatibility means freedom in the selection of components - even the most powerful ones that require really high-end cooling.</p>
                <h3>EFFECTIVE DUST BARRIER</h3>
                <p>Dust penetrating the inside of the case is the nightmare of every computer system. With Fury Shobo SH4F you dont have to worry about that anymore. The housing is completely filtered against dust: from the top and bottom, and the "mesh" front has very dense meshes with a diameter clearly below 1 mm, providing protection against dirt and facilitating free air flow. Dust collecting on the surface of the mesh filters can be quickly and easily removed using a regular cloth or brush.</p>
                <h3>GREAT POSSIBILITIES OF A SMALL HOUSING</h3>
                <p>While maintaining small external dimensions, the Shobo SH4F case offers full compatibility with ATX, micro-ATX and mini-ITX boards. It can accommodate a powerful graphics card up to 330 mm long, up to 3 drives/media (HDD/SSD) and a CPU air cooler up to 161 mm. The two-chamber design with a "basement" for the power supply and numerous cable entries means no mess and easy organization of components.</p>  
                <h3>YOUR COMMAND CENTER</h3>
                <p>Dont let yourself be limited! The richly equipped top panel will allow you to connect the necessary accessories, such as a camera, pendrive or external drive. There you will find 3 USB-A ports (2 of which are fast USB 3.0, 5 Gbit/s), HD Audio 3.5 mm connectors for headphones and a microphone, power and hard drive LEDs, and power and reset buttons.</p>
                <h3>INVINCIBLE POWER, MODERN DESIGN</h3>
                <p>Feast your eyes and show off your equipment to other players! The futuristic, geometric shape will appeal to both hardcore gamers and supporters of a more subdued design. The left side panel made of tempered glass allows you to display the inside of the case and the powerful components hidden inside - also with RGB.</p>""",
            "sale_id": 3,
        },
        {
            "id": 22,
            "name": "Modecom Siroco ARGB FLOW Midi",
            "price": 75.0,
            "old_price": 85.0,
            "description": """<h3>MODECOM Siroco ARGB FLOW MIDI</h3>
                <p>If you dream of an efficient and well-functioning computer, you can choose a computer case such as MODECOM Siroco for your dream components. Inside you will find four 140 mm ARGB fans, an ARGB fan controller and practical solutions for building a computer. There are plenty of airy panels for optimal air circulation, and there is also plenty of space for a high CPU cooler and long graphics cards.</p>
                <p>A side panel made of tempered glass in the form of an opening door makes it very convenient to assemble and clean the computer. You can open the door and install components in a simple and convenient way, as well as easily display your configuration. On the top panel of the MODECOM Siroco case you will also find numerous ports, such as USB-C.</p>
                <h3>MODECOM Siroco ARGB FLOW MIDI</h3>
                <p>A place for everything you need</p>
                <p>You can mount up to 6 hard drives in the MODECOM Siroco housing. Its up to you whether you want to install them in a 5x SSD and 1x HDD or 4x SSD and 2x HDD configuration. With gaming graphics cards in mind, the housing is designed to accommodate models with a maximum length of up to 345 mm. The interior of the case also offers space for a CPU cooler up to 180 mm high. There is nothing stopping you from installing a CPU water cooler with a radiator up to 360 mm in size. In the MODECOM Siroco housing, you can mount the power supply in a dedicated tunnel, ensuring optimal and uninterrupted operation. Its maximum length with the mounted disk basket is 210 mm.</p>
                <p>Stylish and efficient cooling</p>
                <p>Airy panels - front and top - are responsible for optimal air flow in MODECOM Siroco. Small openings at the front effectively bring in cool air while keeping dust particles out, while vents at the back and top dissipate heat. Four pre-installed 140 mm ARGB fans guarantee optimal air circulation around all components.</p>
                <p>You can set the backlight color and rotation speed of the installed ARGB fans using the built-in ARGB controller. This gives you even greater options for configuring your computer. The controller allows you to connect up to 5 fans in total.</p>""",
            "sale_id": None,
        },
        {
            "id": 23,
            "name": "Phanteks NV5 ARGB Tempered Glass White",
            "price": 110.0,
            "old_price": 120.0,
            "description": """<h3>Immerse yourself in the world of optimal ventilation and extravagant design with the Phahnteks NV5 case!</h3>
                <p>Phahnteks NV5 is a case designed without compromise when it comes to cooling the components of your PC and its appearance. The upper and side parts of the housing are equipped with a delicate mesh, creating ideal conditions for ensuring adequate air circulation.</p>
                <p>The characteristic element of NV5 is the front and side panel, which are made of tempered glass. The large panel of pieces not only looks stunning in itself, but is a perfect way to display the inside of your computer. Integrated ARGB lighting on the power supply cover allows you to give your system a unique character by illuminating it in the colors of your choice.</p>
                <h3>Impressive airflow</h3>
                <p>When designing the NV5, Phanteks focused on component cooling from the very beginning. The housing is optimized for free air flow. The upper part and one of the side panels are made of mesh ensuring effective air circulation. There is an option to install a fan at the bottom, providing an additional source of fresh air.</p>
                <p>In addition, NV5 allows you to install up to seven 120 mm fans, which guarantees effective cooling at all times. The side wall allows for three fans, the top also accommodates three, and the rear wall accommodates one fan. Additionally, at the bottom of the housing there is space for another fan. Another advantage is the inclined power supply chamber, which improves air circulation at the bottom of the case.</p>
                <h3>Many mounting options for radiators and water cooling</h3>
                <p>If you plan to equip your system with water cooling, the NV5 is the perfect choice. You can place a 360 mm radiator either on the side or on the top of the case. Additionally, there is room for a 120 mm radiator on the back, which is useful if you want to install a small AiO cooler to cool the CPU.</p>
                <h3>Lots of space for gaming equipment</h3>
                <p>NV5 is a spacious case in many respects. You can easily install three 3.5" drives or 4 2.5" drives or a very long ATX power supply (up to 230mm). It is also not afraid of high CPU coolers (up to 180mm)</p>
                <p>The case also supports the installation of E-ATX motherboards and graphics cards with a maximum length of 440mm. Vertical installation is also possible (mounting elements available separately).</p>
                <p>In addition to the standard Power button, the I/O panel also includes an HD-Audio and microphone port, as well as a USB 3.1 Type C port and two USB 3.0 Type A ports, which enable fast data transfer. Additionally, there are two buttons to control ARGB lighting.</p>""",
            "sale_id": None,
        },
        {
            "id": 24,
            "name": "Logic Portos Midi ARGB Black",
            "price": 50.0,
            "old_price": 64.0,
            "description": """<h3>Logic Portos ARGB Midi Black case</h3>
                <p>Build an efficient and modern gaming computer with Logic Portos ARGB Midi. The device ensures good air flow, smooth operation of components, their safety and low temperatures inside. A side panel made of tempered glass in the form of a door placed on hinges not only facilitates the installation of components, but also allows you to keep the computer clean.</p>
                <p><em>The offer applies only to the case with pre-installed fans. Other components visible in the photo are not part of the set.</em></p>
                <h3>Logic Portos ARGB Midi Black case</h3>
                <p>Cool interior</p>
                <p>The airy front and top panel significantly facilitates air circulation. Three 120 mm fans at the front and one 120 mm fan at the back of the Logic Portos ARGB Midi case effectively cool heated components. Everything for your comfort and computer security. Installed dust filters protect the interior from dust, even when the computer is turned off.</p>
                <p>Easy assembly of components</p>
                <p>Logic Portos ARGB Midi allows for mounting graphics cards up to 340 mm and CPU cooling up to 155 mm. The maximum length of the power supply with the installed disk basket is 200 mm. 7 slots for PCIe expansion cards are the optimal number for mounting, among others: graphics card and network card. You can also install a total of five SSDs and one HDD or four SSDs and two HDDs inside.</p>""",
            "sale_id": None,
        },
        {
            "id": 25,
            "name": "Lian Li Lancool 205 Mesh C ARGB Tempered Glass White",
            "price": 105.0,
            "old_price": 110.0,
            "description": """<h3>Lian Li LANCOOL 205 Mesh C White Computer Case</h3>
                <p>Building an efficient system doesnt have to be difficult. The Lian Li LANCOOL 205 Mesh C case offers a spacious interior where you can accommodate numerous components. Additionally, it ensures worry-free ventilation performance with its pre-installed fans and mesh front panel. The white design will stand out at your gaming station. The manufacturer has installed two switches to control the modes and colors of the ARGB lighting.</p>
                <h3>Lian Li LANCOOL 205 Mesh C White Computer Case</h3>
                <p>Spacious Interior</p>
                <p>The Lian Li LANCOOL 205 Mesh C is a Midi Tower design, offering ample space for installing components such as ATX, Micro-ATX, and Mini-ITX motherboards. It can accommodate graphics cards up to 350 mm in length. You can install two 2.5-inch SSDs on separate mounts behind the motherboard tray. Additionally, it can house several other 2.5" and 3.5" drives. The case can fit an ATX power supply up to 165 mm in depth.</p>
                <p>Excellent Cooling and Ventilation</p>
                <p>Dont worry about high temperatures inside the Lian Li LANCOOL 205 Mesh C case. It comes equipped with factory-installed ARGB PWM 140 mm fans at the front and one 120 mm fan at the back. Additionally, it features a mesh front panel and numerous ventilation holes for efficient airflow.</p>
                <p>The 205 Mesh C also offers extensive options for expanding the cooling system. You can install additional fans as well as water cooling with a radiator up to 280 mm.</p>""",
            "sale_id": None,
        },
        {
            "id": 26,
            "name": "Logic Aramis Midi ARGB Black",
            "price": 50.0,
            "old_price": 60.0,
            "description": """<h3>Logic Aramis ARGB Midi Black Computer Case</h3>
                <p>Logic Aramis ARGB is a case that was created to build an efficient and modern gaming computer. It provides optimal airflow and has pre-installed ARGB fans, which make it a gaming device. Additionally, practical solutions allow for convenient installation of the released components inside. Tempered glass on the side allows you to display the components, positively influencing the design of the entire structure.</p>
                <h3>Logic Aramis ARGB Midi Black Computer Case</h3>
                <p>Well-thought-out cooling system</p>
                <p>The ventilated front panel provides air flow thanks to four efficient 120 mm fans. This allows you to effectively cool the installed components inside the Logic Aramis chassis. You can also install two 140 mm fans on the front of the case, instead of the factory-installed ones.</p>
                <p> Prepared for the installation of efficient components</p>
                <p>Despite its gaming origins, the Logic Aramis ARGB case will also work well in office tasks and everyday work. The ability to build a universal and efficient computer is undoubtedly its advantage. The interior allows for the installation of a graphics card up to 340 mm, and the maximum height of the CPU cooler can be 155 mm.</p>
                <p>Moreover, Logic Aramis Midi allows you to install HDD or SSD drives. At the tunnel level there is a basket for two 3.5" drives or one 3.5" and one 2.5". It is possible to install two additional 2.5" drives on the motherboard tray and two additional 2.5" drives on the wall assembly.</p>""",
            "sale_id": None,
        },
        {
            "id": 27,
            "name": "Logic Aramis Mini ARGB White",
            "price": 40.0,
            "old_price": 60.0,
            "description": """<h3>Logic Aramis ARGB Mini White Case</h3>
                <p>Logic Aramis ARGB Mini is a case designed to build an efficient and modern gaming computer. Optimal airflow, practical solutions, and factory-installed ARGB fans ensure not only an appropriate working environment but also a gaming-like appearance of the station.</p>
                <h3>Logic Aramis ARGB Mini White Case</h3>
                <p>Cool interior of the case</p>
                <p>The ventilated front panel provides airflow thanks to two efficient 120 mm fans. This allows you to effectively cool the installed components inside Logic Aramis ARGB Mini, positively influencing their work culture and durability. Optionally, you can install up to two 140 mm fans on the front of the case, instead of the factory-installed ones.</p>
                <p>Convenient installation of components</p>
                <p>The Logic Aramis ARGB Mini housing enables the installation of graphics cards up to 290 mm and a CPU cooler up to 160 mm. It also allows the installation of HDD or SSD drives. At the tunnel level, there is a basket for a 2.5/3.5" drive and one 3.5" drive. In turn, it is possible to install an additional x 2.5" drive on the motherboard tray. Four PCIe expansion card slots allow you to install additional accessories.</p>
                <p>Gaming nature</p>
                <p>As befits a gaming computer case, Logic Aramis has tempered glass on the side of the case. This makes the inside of the computer clearly visible. Additionally, pre-installed ARGB fans add beauty to the case and gaming station. You can freely change the backlight color from predefined settings using the RESET button on the housing control panel.</p>""",
            "sale_id": None,
        },
        {
            "id": 28,
            "name": "ENDORFY Arx 500 ARGB Tempered Glass",
            "price": 70.0,
            "old_price": 80.0,
            "description": """<h3>ENDORFY Arx 500 ARGB Case</h3>
                <p>Housings are our middle name. Weve been on this topic for years and its hard to impress us, but the sight of ENDORFY Arx 500 ARGB gives us goosebumps. Its out of pride - although some say its because of the low temperature inside the housing.</p>
                <p>We have included our best solutions (including 4 Stratus 140 PWM ARGB). As a result, you get one of the largest (486×228×429 mm, i.e. slightly shorter than the Arx 700 series) ENDORFY cases - with room for a tall cooling system (up to 179 mm), 7 fans and most available graphics cards (up to 350 mm). The outside is also great - with a tempered glass window and front and top panels that act as filters, our ENDORFY Arx 500 ARGB can become a housing master.</p>
                <h3>Come get some fresh air!</h3>
                <p>We all know that long hours at work and on the battlefield (yes, there is a difference) = welded components that beg for a break over time. With the Arx 500 ARGB you dont have such actions - the housing helps keep them pleasantly cool even when you take out the components as much as the factory provided.</p>
                <p>This is due to the spacious interior, which can accommodate as many as 7 air conditioners and fans. Additionally, the housing panels act as filters - so you dont need additional protection against dust. Compared to traditional solutions, this single layer allows for better air circulation and makes it easier to keep the components in a pleasant draft (because cooling is extremely important to us).</p>
                <h3>The Lord of the Rings of the Gales</h3>
                <p>When you look inside the Arx 500 ARGB, you immediately see that there is a specific team of cooling fans working inside. We packed 4 Stratus 140 PWM ARGBs in it - created in cooperation with Synergy Cooling, so you can be sure of adequate air flow and low temperature. Because winter never surprises us.</p>
                <p>The Stratus 140 PWM ARGB is our favorite. Its 14 cm tall, has an optional semi-passive mode and a durable FDB bearing, so you can count on quiet and smooth operation even in extreme conditions. We also added a splitter to control the fan speed using a PWM signal from one motherboard connector. With such a package, you are like a real Lord of the Rings of the Gales.</p>
                <h3>Panels with filters <3</h3>
                <p>If we were to talk about the best - in our opinion - option in the Arx 500 ARGB, we would choose excellent ventilation. This is provided, among others, (right after great fans) by panels made of finely perforated sheet metal. Some people will probably say that they can be replaced with put-on filters - but the truth is that the double anti-dust layer limits the air flow like metal armor in LARPs.</p>
                <p>And no one likes to have welded... components.</p>
                <p>Thats why we made sure that the panels (front and top) in our case act as filters. This single protective layer makes the inside of the case as cool as a winter morning, and you dont have to install additional dust protection. Additionally, you can remove each filter and clean it with a cloth or a vacuum cleaner (or rinse it under running water) - and it will take you literally a moment.</p>
                <h3>Mister of casings</h3>
                <p>Weve already said it, but well say it again - if there is ever a Mr. Housing election, the Arx 500 ARGB has a chance to be on the podium. All we need to do is turn on the ARGB-lit fans inside and the title is ours. The tempered glass side highlights them like a dream.</p>
                <h3>Everythings all right!</h3>
                <p>If someone asked us to describe the Arx 500 ARGB in three words, we would say: "Everything is fine!" Literally - its one of our largest cases, so it easily fits everything thats most important to you. Of course, we mean components.</p>
                <p>Arx 500 ARGB is 486×228×429 mm, so you can pack a lot inside - for example, a tall cooling system (up to 179 mm), 7 fans (including 4 you get from us at the start) and most graphics cards available on the market (up to 350mm). There will also be a large power supply - you can mount it in the position that is most convenient for you. Its installation is not a philosophy, because we have added, among other things, a dedicated mounting frame.</p>
                <h3>Light at the end of the housing tunnel</h3>
                <p>Equipment without backlight is ok, but its nice to see the light at the end of the tunnel sometimes. With Arx 500 ARGB you have this option - with just one click (the RESET button on the top of the housing is responsible for control), your components will be illuminated with a cosmic glow. Thank your ARGB fans for that.</p>
                
                <p>Thanks to 4 Stratus 140 PWM ARGB lights (we installed them in the housing for you), you can freely configure the backlight. You can set them up in just a moment thanks to the built-in PWM and ARGB controllers - everything is immediately connected into one working whole, compatible with ENDORFY products with the ARGB mark (and compatible products from other manufacturers), so you can easily synchronize the backlight of the entire set based on Arx 500 ARGB.</p>""",
            "sale_id": None,
        },
        {
            "id": 29,
            "name": "AiO Arctic Liquid Freezer II 280 OUTLET water",
            "price": 44.0,
            "old_price": 50.0,
            "description": """<h3>Arctic Liquid Freezer II 280: Efficient liquid cooling for gaming computers</h3>
                <p>Powerful computers require efficient components, and in such cases, liquid cooling becomes necessary. One of the best solutions of this type is Arctic Liquid Freezer II 280, which provides not only excellent performance, but also low noise level.</p>
                <h4>New, improved pump</h4>
                <p>The Arctic Liquid Freezer II 280 cooler uses a new, improved pump that ensures high CPU cooling efficiency with minimal noise. Thanks to the manufacturers years of experience in the field of liquid cooling, this pump is reliable and effective even in the most demanding conditions.</p>
                <h4>Tidy in the housing</h4>
                <p>The extremely aesthetic Arctic Liquid Freezer II 280 cooler not only ensures the appropriate temperature of computer components, but also keeps the case tidy. Thanks to integrated cable management, the inside of the computer remains clean and tidy, which is important for aesthetics and airflow.</p>
                <h4>Efficient fans</h4>
                <p>Arctic Liquid Freezer II 280 is equipped with two P-type fans that guarantee fast heat transfer thanks to their high static and efficiency. Additionally, a 40 mm fan located next to the pump helps cool the VRM systems, which prevents overheating even during intensive use.</p>
                <p>The minimum fan speed is 800 rpm, and the maximum - 2000 rpm.</p>
                <h4>High quality workmanship and warranty</h4>
                <p>The Arctic Liquid Freezer II 280 radiator is made of high-quality aluminum and copper alloys, which guarantees effective heat dissipation. This cooler is compatible with Intel and AMD sockets, which makes it universal and easy to install.</p>
                <p>Arctic Liquid Freezer II 280 is covered by an impressive 72-month warranty, which ensures its reliability and durability.</p>""",
            "sale_id": None,
        },
        {
            "id": 30,
            "name": "AiO ENDORFY Navis F280 OUTLET",
            "price": 45.0,
            "old_price": 56.0,
            "description": """<h3>Endorfy Navis F280: High-Efficiency AIO Liquid Cooling Solution</h3>
                <p>Get ready for top-tier cooling performance without the hassle of fan noise with the Endorfy Navis F280 AIO liquid cooling set. Designed to meet the demands of even high-energy processors, this cooling solution ensures efficient heat dissipation to keep your system running smoothly.</p>
                <h4>Efficient Pump and Fluctus Fans</h4>
                <p>The central component of the Navis F280 is its block pump featuring a ceramic bearing and PWM control, ensuring optimal performance and quiet operation. Paired with two Fluctus 140mm fans, which operate at lower speeds while delivering excellent cooling performance, this AIO liquid cooling set guarantees efficient heat dissipation without unnecessary noise.</p>
                <h4>Quiet Operation</h4>
                <p>The Navis F280 is engineered for whisper-quiet operation, allowing you to focus on your tasks or gaming sessions without being disturbed by fan noise. The Fluctus fans are designed with precisely profiled blades to cover the radiator fins effectively, reducing noise levels to a minimum. Additionally, the wavy edge design further minimizes noise for a peaceful computing experience.</p>
                <h4>Exceptional Cooling Efficiency</h4>
                <p>With its specially designed asymmetric water block and efficient pump with PWM control, the Navis F280 offers one of the best cooling efficiencies in its class. Whether youre working or gaming, this cooling solution ensures that your system remains cool and quiet, even during extended use.</p>
                <h4>Flexible Installation Options</h4>
                <p>The Navis F280 features flexible hoses, allowing you to install the cooler in any position inside your computer for maximum convenience. The approximately 39 cm long hoses provide ample flexibility for hassle-free installation.</p>
                <h4>Included Pactum PT-3 Thermal Paste</h4>
                <p>The package includes a tube of Pactum PT-3 thermal paste, ensuring efficient heat transfer between the CPU and the water block. With this high-quality thermal paste, you can enjoy worry-free installations and optimal cooling performance.</p>
                <p>Please note that this item comes from a consumer return and may exhibit normal signs of use and/or damaged packaging. However, rest assured that the equipment is thoroughly checked and fully functional.</p>""",
            "sale_id": 4,
        },
            {
            "id": 31,
            "name": "AiO Arctic Liquid Freezer III 420 Black",
            "price": 75.0,
            "old_price": 80.0,
            "description": """<h3>Liquid Freezer III: High-Performance Cooling Solution</h3>
                <p>The Liquid Freezer III is the perfect solution for demanding users seeking excellent performance and whisper-quiet operation. With its new, optimized CPU power section fan and increased water channels, this cooling system ensures stable temperatures even under heavy loads.</p>
                <h4>Efficient Cooling for Enthusiasts</h4>
                <p>Designed for computer enthusiasts, the Liquid Freezer III offers simple installation and exceptional efficiency. The improved VRM fan provides near-silent ventilation, prolonging the lifespan of components and maintaining optimal performance.</p>
                <h4>Ready-to-Use AiO Kit</h4>
                <p>The Liquid Freezer III comes ready to use straight out of the box, making it hassle-free to set up. With a wide range of variants available, including different heatsink sizes and lighting options, theres a Liquid Freezer III model to meet the needs of even the most discerning users.</p>
                <h4>Modern Design and Performance</h4>
                <p>Combining modern design with high performance, the Liquid Freezer III is the ideal choice for those who prioritize aesthetics and functionality. Whether youre a gamer, content creator, or power user, this cooling solution offers the perfect balance of style and performance.</p>""",
            "sale_id": None,
        },
        {
            "id": 32,
            "name": "AiO Arctic Liquid Freezer III 420 ARGB White",
            "price": 100.0,
            "old_price": 120.0,
            "description": """<h3>The Liquid Freezer III: Ultimate Cooling Performance</h3>
                <p>The Liquid Freezer III is the perfect solution for demanding users who require excellent performance and silent operation. Equipped with a new, optimized CPU power section fan and an increased number of water channels, the Liquid Freezer III ensures stable temperatures even under heavy loads.</p>
                <h4>Designed for Enthusiasts</h4>
                <p>This cooling system is tailored for computer enthusiasts, offering straightforward installation and exceptional efficiency. The upgraded VRM fan delivers near-silent ventilation, promoting longevity for your components.</p>
                <h4>Ready-to-Use All-in-One Kit</h4>
                <p>With the Liquid Freezer III, you can start cooling your system right out of the box. It comes in a variety of versions, featuring different heatsink sizes and lighting options, catering to the needs of the most discerning users.</p>
                <h4>Modern Design and Superior Performance</h4>
                <p>The Liquid Freezer III combines sleek, modern design with unparalleled performance. Whether you prioritize aesthetics or functionality, this cooling solution delivers on both fronts, making it the ideal choice for users who demand the best.</p>""",
            "sale_id": None,
        },
        {
            "id": 33,
            "name": "AiO EK Water Blocks EK-Nucleus CR360 Lux D-RGB White 360mm",
            "price": 170.0,
            "old_price": 200.0,
            "description": """<h3>EK-Nucleus AIO Lux Liquid Cooling: Exceptional Design and Performance Awarded iF Design Award</h3>
                <p>Elegant and innovative - EK-Nucleus AIO Lux, winner of the prestigious iF Design award, is a real breakthrough in the field of liquid cooling. Designed specifically for the latest Intel® 13th Gen (LGA 1700) and AMD® Ryzen™ 7000 (AM5) processors, it provides ultra-low temperatures, backed by a 5-year warranty for complete peace of mind.</p>
                <h4>Elegance in Two Colors</h4>
                <p>Available in black and white, the EK-Nucleus AIO Lux not only looks great, but also offers full customization with addressable D-RGB lighting. The tunnel light effect on the pump cover turns your system into a real symphony of light. The cooling system is also equipped with aesthetic braided hoses.</p>
                <h4>Easy Installation</h4>
                <p>With EK-Nucleus, installation becomes childs play. Universal compatibility includes the latest processors on AM5 and LGA 1700 sockets, and installation is hassle-free thanks to tool-free pump assembly, a modern EK-OmniLink connector and aluminum swivel connectors. Once installed, the Nucleus AIO requires no maintenance as it comes pre-filled with coolant.</p>
                <h4>Individual Symphony of Light (or Darkness)</h4>
                <p>With fully customizable D-RGB lighting, you can personalize your AiO EK-Nucleus to match your PC setup. A spectrum of colors, smooth transitions and effects that change with one click. Compatibility with RGB software such as ASUS Aura Sync, Gigabyte RGB Fusion 2 and MSI Mystic Light enables even wider possibilities.</p>
                <p>Dont like RGB? No worries! EK-Nucleus AIO Dark is a black, light-free option for those who prefer a dark style for their PC.</p>
                <h4>Built on 15+ Years of Liquid Cooling Experience</h4>
                <p>With over 15 years of experience in the liquid cooling industry, EK-Nucleus AIO ensures ultra-low temperatures even during the most intense gaming sessions.</p>
                <h4>Quiet Operation, High Efficiency</h4>
                <p>EK-Nucleus AIO offers not only performance, but also quiet operation, thanks to the latest EK-Loop FPT fans and intelligent cable integration using the EK-OmniLink system.</p>
                <h4>Highest Quality without Compromise</h4>
                <p>EK-Nucleus is synonymous with the highest quality. Meticulous quality control, rigorous production process and modern technology combine to deliver a product with extraordinary durability and reliability. This is also confirmed by a long, 5-year manufacturers warranty.</p>""",
            "sale_id": None,
        },
        {
            "id": 34,
            "name": "CPU Valkyrie Vind SL125 Białe",
            "price": 50.0,
            "old_price": 60.0,
            "description": """<h3>Valkyrie Vind SL125 White: Efficient Air Cooling for Demanding Tasks</h3>
                    <p>The Valkyrie Vind SL125 White offers a white air cooling solution designed to tackle even the most demanding challenges. With perfect heat distribution, high-performance fans, and a powerful radiator, this cooler ensures your processor stays cool during intense gaming and strenuous tasks.</p>
                    <h4>Advanced Heat Exchanger Design</h4>
                    <p>The Valkyrie Vind SL125 White features a specially designed heat exchanger with six copper heat pipes and a copper base, ensuring quick and effective heat dissipation to the radiator.</p>
                    <p>The dense fins on the heat sink ensure high efficiency, while their regular placement minimizes air flow resistance, resulting in exceptionally low temperatures.</p>
                    <h4>Powerful Cooling Fans</h4>
                    <p>The Valkyrie X12 fans provide powerful air circulation, with a blade design that maximizes airflow (80 CFM) at high static pressure (3.14 mm H2O). Despite their high performance, these fans operate quietly at just 29 dBA.</p>
                    <h4>Customizable RGB Lighting</h4>
                    <p>Enhancing its aesthetic appeal, the cooler features addressable RGB lighting integrated into both the heat sink and fans. With the dedicated Valkyrie software, users can personalize the backlight to match their mood, other components, or favorite games.</p>
                    <h4>Easy Installation and Compatibility</h4>
                    <p>The Valkyrie Vind SL125 White kit is compatible with most popular AMD and Intel processors, offering easy installation and support for AM5, AM4, and various Intel sockets including LGA 1700, 1200, 1151, 1150, 1155, and 1156. The kit includes all necessary elements for assembly, including thermal paste.</p>""",
            "sale_id": None,
        },
        {
            "id": 35,
            "name": "CPU Valkyrie Vind SL125 Czarne",
            "price": 55.0,
            "old_price": 65.0,
            "description": """<h3>Valkyrie Vind SL125 Black: Powerful Air Cooling for Demanding Tasks</h3>
                <p>The Valkyrie Vind SL125 Black offers an air cooling solution designed to tackle the most challenging tasks. With perfect heat distribution, high-performance fans, and a powerful radiator, this cooler ensures your processor remains cool during intense gaming sessions and demanding tasks.</p>
                <h4>Advanced Heat Exchanger Design</h4>
                <p>The Valkyrie Vind SL125 Black features a specially designed heat exchanger with six copper heat pipes and a copper base, ensuring quick and effective heat dissipation to the radiator.</p>
                <p>The dense fins on the heat sink ensure high efficiency, while their regular placement minimizes air flow resistance, allowing for very low temperatures.</p>
                <h4>Powerful Cooling Fans</h4>
                <p>The Valkyrie X12 fans provide powerful air circulation, with a 120 mm blade design that delivers maximum airflow (80 CFM) at high static pressure (3.14 mm H2O). Despite their high performance, these fans operate quietly at just 29 dBA.</p>
                <h4>Customizable RGB Lighting</h4>
                <p>Enhancing its aesthetic appeal, the cooler features addressable RGB lighting integrated into both the heat sink and fans. With the dedicated Valkyrie software, users can personalize the backlight to match their mood, other components, or favorite games.</p>
                <h4>Easy Installation and Compatibility</h4>
                <p>The Valkyrie Vind SL125 Black kit is compatible with most popular AMD and Intel processors, offering easy installation and support for AM5, AM4, and various Intel sockets including LGA 1700, 1200, 1151, 1150, 1155, and 1156. All necessary elements for assembly, including thermal paste, are included in the kit.</p>""",
            "sale_id": None,
        },
        {
            "id": 36,
            "name": "Jonsbo CR-1400 CPU ARGB 92mm Black",
            "price": 20.0,
            "old_price": 30.0,
            "description": """<h3>Jonsbo CR-1400: Effective CPU Cooler with Elegant Design</h3>
                <p>Elevate your processors performance with the Jonsbo CR-1400, a potent cooler that not only safeguards your components from overheating but also adds a touch of elegance to your computer setup. Learn why the Jonsbo CR-1400 is the preferred choice for gaming enthusiasts and IT professionals alike.</p>
                <h4>Powerful Cooling with Stylish Design</h4>
                <p>The Jonsbo CR-1400 boasts a sleek black and silver tower design that not only delivers exceptional performance but also stands out visually. Featuring a quiet 92mm PWM fan with ARGB illumination, this cooler effectively maintains CPU temperatures while adding a stylish flair to your system.</p>
                <h4>Details of Jonsbo CR-1400 - Power and Elegance Combined</h4>
                <p>The Jonsbo CR-1400 is a robust tower cooler designed for both AMD and Intel processors. Four copper heat pipes ensure rapid heat dissipation, while the included 92mm fan with ARGB LEDs provides eye-catching illumination. The PWM fan operates at speeds ranging from 900 to 2300 rpm, delivering a maximum noise level of just 30.5 db(A) with an airflow volume of 61.1 m³/h.</p>
                <p>This tower cooler features integrated ARGB lighting on the top cover and fan, with lighting control available through compatible motherboards. The Jonsbo CR-1400 is compatible with a wide range of popular sockets from both AMD and Intel platforms.</p>
                <p>Choose the Jonsbo CR-1400 and experience not only enhanced thermal performance for your processor but also the modern, designer aesthetic for your computer setup. Discover the perfect blend of cooling power and style with the Jonsbo CR-1400!</p>""",
            "sale_id": None,
        },
        {
            "id": 37,
            "name": "Noctua NH-U14S 140mm",
            "price": 120.0,
            "old_price": 130.0,
            "description": """<h3>Noctua NH-U14S: Exceptional Performance, Reliability, and Low Noise</h3>
                <p>The Noctua NH-U14S stands out as one of the premier CPU coolers available on the market, renowned for its outstanding performance, reliability, and minimal noise output, making it an ideal solution for even the most demanding users.</p>
                <p>Designed with the latest processors in mind, the NH-U14S effectively dissipates heat generated during intensive use, ensuring long-term stability and optimal performance. This cooling solution features six copper heat pipes encased in an aluminum frame, enabling excellent airflow and efficient cooling for even the most demanding processors.</p>
                <p>The NH-U14S is equipped with the NF-A15 PWM fan, renowned for its exceptional performance and minimal noise levels. Enhanced with advanced technologies like AAO Frame and SSO2 Bearing, this fan delivers high efficiency and longevity, ensuring reliable operation over extended periods.</p>
                <p>In addition to its exceptional performance, the NH-U14S boasts an elegant design that seamlessly complements any computer setup. With dimensions of 165 x 150 x 52 mm and a weight of only 935 g, this cooler is both compact and easy to install, making it a practical choice for users seeking both performance and convenience.</p>
                <p>In summary, the Noctua NH-U14S offers unparalleled performance, stability, and aesthetics for users who demand the best from their computer cooling solutions. With advanced technological features and a sleek design, the NH-U14S sets the standard for CPU cooling</p>""",
            "sale_id": None,
        },
        {
            "id": 38,
            "name": "ENDORFY Spartan 5 MAX ARGB",
            "price": 25.0,
            "old_price": 35.0,
            "description": """<h3>ENDORFY Arx 500 ARGB: Elevate Your PC Experience with Style and Performance</h3>
                <p>When it comes to PC casings, ENDORFY has been a household name for years. But the sight of the ENDORFY Arx 500 ARGB still gives us goosebumps - not just out of pride, but because of the cool temperatures it maintains inside.</p>
                <p>Featuring our best solutions, including 4 Stratus 140 PWM ARGB fans, the ENDORFY Arx 500 ARGB offers ample space for tall cooling systems, up to 7 fans, and most available graphics cards. With dimensions of 486×228×429 mm, its slightly shorter than the Arx 700 series but packs just as much punch.</p>
                <h3>Come Get Some Fresh Air!</h3>
                <p>The Arx 500 ARGB ensures your components stay pleasantly cool even during long gaming sessions or intense workloads. With space for up to 7 fans and integrated panel filters, it provides excellent airflow without the need for additional dust protection.</p>
                <h3>The Lord of the Rings of the Gales</h3>
                <p>The Arx 500 ARGB comes equipped with 4 Stratus 140 PWM ARGB fans, ensuring optimal airflow and low temperatures. These fans, created in collaboration with Synergy Cooling, feature a durable FDB bearing and optional semi-passive mode for quiet operation even under extreme conditions.</p>
                <h3>Panels with Filters <3</h3>
                <p>Our finely perforated sheet metal panels act as filters, ensuring excellent ventilation without restricting airflow. These panels, located on the front and top of the case, can be easily removed and cleaned, keeping your components cool and dust-free.</p>
                <h3>Mister of Casings</h3>
                <p>If there were ever a "Mr. Housing" contest, the Arx 500 ARGB would be a strong contender. With its ARGB-lit fans and tempered glass side panel, its a sight to behold.</p>
                <h3>Everythings All Right!</h3>
                <p>In three words, the Arx 500 ARGB can be described as "Everything is fine!" With ample space for components, stylish design, and customizable ARGB lighting, its the perfect housing solution for any PC enthusiast.</p>
                <h3>Light at the End of the Housing Tunnel</h3>
                <p>With the Arx 500 ARGB, you can bring your PC to life with customizable ARGB lighting. Control the lighting with a single click and synchronize it with other ENDORFY ARGB products for a cohesive look.</p>""",
            "sale_id": None,
        },
        {
            "id": 39,
            "name": "Lexar 1TB M.2 PCIe Gen4 NVMe NM800 Pro",
            "price": 125.0,
            "old_price": 135.0,
            "description": """<h3>Lexar 1TB M.2 PCIe Gen4 NVMe NM800 Pro: High-Speed Storage for Enhanced Performance</h3>
                <p>The Lexar 1TB M.2 PCIe Gen4 NVMe NM800 Pro is a top-of-the-line solid-state drive (SSD) designed to deliver exceptional speed and reliability for demanding computing tasks. With its PCIe Gen4 interface and NVMe protocol support, this SSD offers blazing-fast read and write speeds, making it an ideal choice for gamers, content creators, and professionals.</p>
                <h3>Exceptional Speed and Performance</h3>
                <p>Featuring cutting-edge PCIe Gen4 technology, the Lexar NM800 Pro SSD delivers sequential read speeds of up to [insert speed] and sequential write speeds of up to [insert speed], significantly reducing load times and improving overall system responsiveness. Whether youre gaming, editing high-resolution videos, or running resource-intensive applications, this SSD ensures smooth performance and accelerated data transfer.</p>
                <h3>Reliable Storage Solution</h3>
                <p>Lexar is renowned for producing high-quality storage solutions, and the NM800 Pro SSD is no exception. Built with premium NAND flash memory and advanced controller technology, this SSD offers durability, reliability, and endurance for long-term usage. Additionally, with its M.2 form factor, the NM800 Pro is compatible with a wide range of desktops, laptops, and ultrabooks, allowing for easy installation and seamless integration into your system.</p>
                <h3>Enhanced Productivity and Efficiency</h3>
                <p>Upgrade your system with the Lexar NM800 Pro SSD and experience faster boot times, quicker application launches, and improved overall system performance. With its large 1TB capacity, youll have ample space to store your operating system, software applications, games, and multimedia files, helping you stay productive and efficient in your daily computing tasks.</p>""",
            "sale_id": None,
        },
        {
            "id": 40,
            "name": "Lexar 1TB M.2 PCIe Gen4 NVMe NM790",
            "price": 105.0,
            "old_price": 115.0,
            "description": """<h3>Lexar 1TB M.2 PCIe Gen4 NVMe NM790: High-Speed Storage Solution</h3>
                <p>The Lexar 1TB M.2 PCIe Gen4 NVMe NM790 is a high-performance solid-state drive (SSD) designed to provide lightning-fast data transfer speeds and reliable storage for demanding computing tasks. With its PCIe Gen4 interface and NVMe protocol support, this SSD offers exceptional performance and efficiency, making it an excellent choice for gamers, content creators, and professionals.</p>
                <h3>Blazing Fast Speeds</h3>
                <p>Equipped with advanced PCIe Gen4 technology, the Lexar NM790 SSD delivers impressive sequential read speeds of up to [insert speed] and sequential write speeds of up to [insert speed], significantly reducing load times and improving overall system responsiveness. Whether youre gaming, editing high-definition videos, or multitasking with resource-intensive applications, this SSD ensures smooth and efficient performance.</p>
                <h3>Reliable Performance</h3>
                <p>Lexar is known for its commitment to quality and reliability, and the NM790 SSD upholds this tradition. Built with premium NAND flash memory and a robust controller, this SSD offers durability, stability, and long-term reliability for continuous usage. Additionally, the M.2 form factor ensures compatibility with a wide range of desktops, laptops, and ultrabooks, allowing for easy installation and seamless integration into your system.</p>
                <h3>Enhanced Productivity</h3>
                <p>Upgrade your system with the Lexar NM790 SSD and experience enhanced productivity and efficiency. With its generous 1TB storage capacity, youll have ample space to store your operating system, applications, games, and multimedia files, allowing you to work, create, and play without limitations. Say goodbye to slow loading times and hello to a smoother computing experience with the Lexar NM790 SSD.</p>""",
            "sale_id": None,
        },
        {
            "id": 41,
            "name": "Lexar 1TB M.2 PCIe Gen4 NVMe NM710",
            "price": 95.0,
            "old_price": 105.0,
            "description": """<h3>Lexar 1TB M.2 PCIe Gen4 NVMe NM710: High-Speed Storage Solution</h3>
                <p>The Lexar 1TB M.2 PCIe Gen4 NVMe NM710 offers lightning-fast data transfer speeds and reliable storage performance, making it an ideal solution for demanding computing tasks. With its PCIe Gen4 interface and NVMe protocol support, this SSD delivers exceptional performance and efficiency, enhancing your overall computing experience.</p>
                <h3>Exceptional Speed and Performance</h3>
                <p>Experience blazing-fast speed and responsiveness with the Lexar NM710 SSD. With read speeds of up to [insert speed] and write speeds of up to [insert speed], this SSD accelerates your system boot-up times, application launches, and file transfers, allowing you to work, play, and create without delays or interruptions.</p>
                <h3>Reliable and Durable</h3>
                <p>Designed for reliability and durability, the Lexar NM710 SSD is built with high-quality NAND flash memory and a robust controller, ensuring long-term performance and stability. Whether youre gaming, editing videos, or multitasking with resource-intensive applications, this SSD delivers consistent and reliable performance, even under heavy workloads.</p>
                <h3>Easy Installation and Compatibility</h3>
                <p>The M.2 form factor of the Lexar NM710 SSD ensures easy installation in compatible desktops, laptops, and ultrabooks. With its compact design and plug-and-play functionality, upgrading your system with this SSD is a hassle-free process. Plus, with a generous 1TB storage capacity, youll have ample space to store your operating system, applications, and multimedia files.</p>
                <h3>Enhanced Productivity</h3>
                <p>Boost your productivity and workflow efficiency with the Lexar NM710 SSD. Whether youre a professional, content creator, or enthusiast gamer, this SSD empowers you to achieve more with faster data access and improved system performance. Say goodbye to slow loading times and hello to a smoother computing experience with the Lexar NM710 SSD.</p>""",
            "sale_id": None,
        },
        {
            "id": 42,
            "name": "Lexar 1TB M.2 PCIe Gen3 NVMe NM620",
            "price": 65.0,
            "old_price": 75.0,
            "description": """<h3>Lexar 1TB M.2 PCIe Gen3 NVMe NM620: Reliable High-Speed Storage</h3>
                <p>The Lexar 1TB M.2 PCIe Gen3 NVMe NM620 SSD offers high-speed performance and reliable storage capacity, making it an excellent choice for upgrading your system. With its PCIe Gen3 interface and NVMe protocol support, this SSD delivers fast data transfer speeds and responsive computing performance for a wide range of applications.</p>
                <h3>Fast Data Transfer Speeds</h3>
                <p>Experience rapid data transfer speeds with the Lexar NM620 SSD. With read speeds of up to [insert speed] and write speeds of up to [insert speed], this SSD accelerates system boot-up times, application launches, and file transfers, allowing you to work and play without delays.</p>
                <h3>Reliable Performance</h3>
                <p>Built with high-quality NAND flash memory and a reliable controller, the Lexar NM620 SSD delivers consistent performance and durability. Whether youre gaming, editing multimedia content, or multitasking with demanding applications, this SSD ensures smooth operation and responsiveness.</p>
                <h3>Easy Installation</h3>
                <p>The M.2 form factor of the Lexar NM620 SSD makes it easy to install in compatible desktops, laptops, and ultrabooks. With its plug-and-play functionality, upgrading your system with this SSD is a simple and hassle-free process, allowing you to enjoy faster performance in no time.</p>
                <h3>Ample Storage Capacity</h3>
                <p>With a generous 1TB storage capacity, the Lexar NM620 SSD provides ample space to store your operating system, applications, games, and multimedia files. Whether youre a professional user or an enthusiast gamer, youll have plenty of room to store your digital content and enjoy faster access to your data.</p>
                <h3>Enhanced Productivity</h3>
                <p>Boost your productivity and workflow efficiency with the Lexar NM620 SSD. Whether youre performing everyday computing tasks or demanding workloads, this SSD enables you to achieve more with its high-speed performance and responsive operation. Say goodbye to slow loading times and hello to improved productivity with the Lexar NM620 SSD.</p>""",
            "sale_id": None,
        },
        {
            "id": 43,
            "name": "MSI 2TB M.2 PCIe Gen4 NVMe Spatium M482",
            "price": 150.0,
            "old_price": 165.0,
            "description": """<h3>MSI 2TB M.2 PCIe Gen4 NVMe Spatium M482: Unleash Next-Level Storage Performance</h3>
                <p>The MSI 2TB M.2 PCIe Gen4 NVMe Spatium M482 SSD is engineered to deliver unparalleled storage performance, reliability, and capacity, elevating your computing experience to new heights. Designed for enthusiasts, gamers, and content creators, this SSD offers lightning-fast data transfer speeds and ample storage space to accommodate your growing digital needs.</p>
                <h3>Unmatched Speed and Efficiency</h3>
                <p>Experience blazing-fast data transfer speeds with the MSI Spatium M482 SSD. Leveraging PCIe Gen4 technology and NVMe protocol support, this SSD achieves read speeds of up to [insert speed] and write speeds of up to [insert speed], ensuring rapid access to your files, applications, and games. Say goodbye to long load times and hello to seamless performance.</p>
                <h3>High-Capacity Storage</h3>
                <p>With a spacious 2TB storage capacity, the MSI Spatium M482 SSD provides ample room to store your operating system, games, multimedia files, and productivity software. Whether youre a content creator working with large video files or a gamer with an extensive library of titles, this SSD offers the storage space you need to keep everything organized and easily accessible.</p>
                <h3>Reliable and Durable</h3>
                <p>Engineered for durability and reliability, the MSI Spatium M482 SSD features high-quality NAND flash memory and a robust controller, ensuring long-term performance and data integrity. Built to withstand the rigors of daily use, this SSD offers peace of mind knowing that your valuable data is safe and secure.</p>
                <h3>Advanced Cooling Design</h3>
                <p>Equipped with an advanced cooling design, the MSI Spatium M482 SSD maintains optimal operating temperatures even during intense workloads. The heat spreader and thermal pads efficiently dissipate heat, preventing thermal throttling and ensuring consistent performance under any workload.</p>
                <h3>Enhanced Productivity and Gaming Experience</h3>
                <p>Boost your productivity and gaming experience with the MSI Spatium M482 SSD. Whether youre editing high-resolution videos, rendering 3D graphics, or enjoying immersive gaming sessions, this SSD accelerates your workflow and enhances overall system responsiveness, allowing you to focus on what matters most.</p>
                <h3>Easy Installation and Compatibility</h3>
                <p>Featuring an M.2 form factor, the MSI Spatium M482 SSD is easy to install in compatible desktops, laptops, and ultrabooks. With its plug-and-play functionality and wide compatibility, upgrading your system with this SSD is a breeze, ensuring a seamless transition to next-level storage performance.</p>""",
            "sale_id": None,
        },
        {
            "id": 44,
            "name": "HIKSEMI Future 1TB M.2 2280 PCI-E x4 Gen4 NVMe",
            "price": 125.0,
            "old_price": 135.0,
            "description": """<h3>HIKSEMI Future 1TB M.2 2280 PCI-E x4 Gen4 NVMe: Redefining Storage Performance</h3>
                <p>Experience the future of storage with the HIKSEMI Future 1TB M.2 2280 PCI-E x4 Gen4 NVMe SSD. Engineered to deliver unparalleled speed, reliability, and efficiency, this SSD revolutionizes your computing experience, whether youre a gamer, content creator, or power user.</p>
                <h3>Next-Level Speed</h3>
                <p>Unlock blazing-fast data transfer speeds with the HIKSEMI Future SSD. Utilizing PCIe Gen4 technology and NVMe protocol, this SSD achieves read speeds of up to [insert speed] and write speeds of up to [insert speed], ensuring lightning-fast access to your data, applications, and games. Say goodbye to lag and hello to seamless performance.</p>
                <h3>High-Capacity Storage</h3>
                <p>With a generous 1TB storage capacity, the HIKSEMI Future SSD provides ample space to store your operating system, games, multimedia files, and productivity software. Whether youre storing large video projects or vast game libraries, this SSD offers the storage capacity you need to stay organized and productive.</p>
                <h3>Reliable and Durable</h3>
                <p>Engineered for durability and reliability, the HIKSEMI Future SSD features premium NAND flash memory and a robust controller, ensuring long-term performance and data integrity. Built to withstand the demands of daily use, this SSD provides peace of mind knowing your data is safe and secure.</p>
                <h3>Advanced Cooling Design</h3>
                <p>Equipped with an advanced cooling design, the HIKSEMI Future SSD maintains optimal operating temperatures even during heavy workloads. The heatsink and thermal pads efficiently dissipate heat, preventing thermal throttling and ensuring consistent performance under any workload.</p>
                <h3>Enhanced Productivity and Efficiency</h3>
                <p>Boost your productivity and efficiency with the HIKSEMI Future SSD. Whether youre multitasking, editing high-resolution videos, or running demanding applications, this SSD accelerates your workflow and enhances system responsiveness, allowing you to accomplish more in less time.</p>
                <h3>Easy Installation and Compatibility</h3>
                <p>Featuring an M.2 2280 form factor, the HIKSEMI Future SSD is easy to install in compatible desktops, laptops, and ultrabooks. With its plug-and-play functionality and wide compatibility, upgrading your system with this SSD is simple and hassle-free, ensuring a seamless transition to next-generation storage performance.</p>""",
            "sale_id": None,
        },
        {
            "id": 45,
            "name": "GOODRAM 2TB 2.5\" SATA SSD CX400",
            "price": 145.0,
            "old_price": 155.0,
            "description": """<h3>GOODRAM 2TB 2.5" SATA SSD CX400: Reliable and High-Capacity Storage Solution</h3>
                    <p>Experience enhanced performance and ample storage capacity with the GOODRAM 2TB 2.5" SATA SSD CX400. Designed to deliver reliable performance and data integrity, this SSD offers a seamless upgrade for your system, whether its a desktop, laptop, or gaming console.</p>
                    <h3>High-Capacity Storage</h3>
                    <p>With a spacious 2TB storage capacity, the GOODRAM CX400 SSD provides plenty of room to store your operating system, applications, games, multimedia files, and more. Enjoy the freedom to store large libraries of media content, software applications, and high-resolution files without worrying about running out of space.</p>
                    <h3>Enhanced Performance</h3>
                    <p>Upgrade your systems performance with the GOODRAM CX400 SSD. Featuring SATA III interface, this SSD delivers impressive read and write speeds, reducing boot times, application loading times, and file transfer durations. Enjoy smoother multitasking and faster data access for improved productivity and efficiency.</p>
                    <h3>Reliable Data Storage</h3>
                    <p>Trust in the reliability and durability of the GOODRAM CX400 SSD. Built with high-quality NAND flash memory and a robust controller, this SSD ensures long-term data integrity and consistent performance. Say goodbye to mechanical hard drives and enjoy the peace of mind knowing your data is safe and secure.</p>
                    <h3>Energy-Efficient Design</h3>
                    <p>The GOODRAM CX400 SSD is designed to operate efficiently, consuming less power than traditional hard drives. With lower power consumption, this SSD helps extend the battery life of laptops and reduces energy costs for desktop systems, making it an environmentally friendly storage solution.</p>
                    <h3>Quiet and Cool Operation</h3>
                    <p>Enjoy quiet and cool operation with the GOODRAM CX400 SSD. Unlike mechanical hard drives, SSDs produce minimal noise and heat during operation, resulting in a quieter and cooler computing experience. Whether youre working, gaming, or streaming media, the CX400 SSD ensures a comfortable and enjoyable user experience.</p>
                    <h3>Easy Installation and Compatibility</h3>
                    <p>Upgrade your system effortlessly with the GOODRAM CX400 SSD. Featuring a standard 2.5" form factor, this SSD is compatible with a wide range of desktops, laptops, and gaming consoles. With its plug-and-play installation and SATA interface, upgrading to the CX400 SSD is simple and hassle-free.</p>
                    <p>Experience the benefits of high-capacity, reliable, and energy-efficient storage with the GOODRAM 2TB 2.5" SATA SSD CX400.</p>""",
            "sale_id": None,
        },
        {
            "id": 46,
            "name": "Crucial 4TB 2.5\" SATA SSD MX500",
            "price": 250.0,
            "old_price": 350.0,
            "description": """<h3>Crucial 4TB 2.5" SATA SSD MX500: High-Capacity Storage for Enhanced Performance</h3>
                    <p>Upgrade your system with the Crucial 4TB 2.5" SATA SSD MX500, offering ample storage capacity and exceptional performance. Designed to deliver fast data access, reliable operation, and energy efficiency, the MX500 SSD is an ideal solution for boosting your systems performance and storage capabilities.</p>
                    <h3>Ample Storage Capacity</h3>
                    <p>With a generous 4TB storage capacity, the Crucial MX500 SSD provides plenty of room to store your operating system, applications, games, multimedia files, and more. Enjoy the freedom to store large collections of media content, software applications, and high-resolution files without worrying about running out of space.</p>
                    <h3>Enhanced Performance</h3>
                    <p>Experience faster boot times, application loading, and file transfers with the Crucial MX500 SSD. Featuring SATA III interface and advanced NAND flash memory, this SSD delivers impressive read and write speeds, accelerating system performance and improving overall responsiveness.</p>
                    <h3>Reliable Data Storage</h3>
                    <p>Trust in the reliability and durability of the Crucial MX500 SSD. Built with 3D NAND technology and a robust controller, this SSD ensures long-term data integrity, consistent performance, and resistance to data corruption and loss. Protect your valuable data and enjoy peace of mind knowing your files are safe and secure.</p>
                    <h3>Energy-Efficient Design</h3>
                    <p>The Crucial MX500 SSD is designed to operate efficiently, consuming less power than traditional hard drives. With lower power consumption, this SSD helps extend the battery life of laptops and reduces energy costs for desktop systems, making it an environmentally friendly storage solution.</p>
                    <h3>Quiet and Cool Operation</h3>
                    <p>Enjoy quiet and cool operation with the Crucial MX500 SSD. Unlike mechanical hard drives, SSDs produce minimal noise and heat during operation, resulting in a quieter and cooler computing experience. Whether youre working, gaming, or streaming media, the MX500 SSD ensures a comfortable and enjoyable user experience.</p>
                    <h3>Easy Installation and Compatibility</h3>
                    <p>Upgrade your system effortlessly with the Crucial MX500 SSD. Featuring a standard 2.5" form factor and SATA interface, this SSD is compatible with a wide range of desktops, laptops, and gaming consoles. With its plug-and-play installation, upgrading to the MX500 SSD is simple and hassle-free.</p>
                    <p>Experience the benefits of high-capacity, reliable, and energy-efficient storage with the Crucial 4TB 2.5" SATA SSD MX500.</p>""",
            "sale_id": None,
        },
        {
            "id": 47,
            "name": "Toshiba P300 1TB 7200obr. 64MB",
            "price": 25.0,
            "old_price": 35.0,
            "description": """<h3>Toshiba P300 1TB 7200 RPM 64MB: Reliable and Efficient Hard Drives</h3>
                <p>The Toshiba P300 1TB hard drive is a solid solution for those seeking a reliable data storage with high capacity and performance. With a rotational speed of 7200 RPM and a 64MB buffer, this hard drive provides fast data transfers and smooth operation even during intensive use.</p>
                <h3>High Capacity and Fast Performance</h3>
                <p>With a capacity of 1TB, the Toshiba P300 drive offers ample space for storing multimedia files, games, programs, and other data. Its high rotational speed and large buffer ensure quick access to data and efficient performance for various tasks.</p>""",
            "sale_id": None,
        },
        {
            "id": 48,
            "name": "Silver Monkey X Sirocco 3x120 mm PWM KIT",
            "price": 24.0,
            "old_price": 40.0,
            "description": """<h2>Optimal Cooling Solution</h2>
                <p>Introducing the Silver Monkey X Sirocco 3x120 mm PWM Kit, the ultimate cooling solution for your PC. Engineered for maximum performance and efficiency, this kit ensures optimal cooling to keep your system running smoothly even under heavy loads.</p>
                <h2>Powerful PWM Fans</h2>
                <p>The kit includes three high-quality 120 mm PWM fans, designed to deliver powerful airflow while maintaining quiet operation. With PWM (Pulse Width Modulation) control, you can adjust the fan speed according to your systems temperature, ensuring efficient cooling without unnecessary noise.</p>
                <h2>Enhanced Airflow</h2>
                <p>Each fan features aerodynamically optimized blades and a unique Sirocco design, maximizing airflow and minimizing turbulence. This results in improved cooling performance and enhanced heat dissipation, keeping your components cool even during intense gaming sessions or CPU-intensive tasks.</p>
                <h2>Easy Installation</h2>
                <p>The Silver Monkey X Sirocco 3x120 mm PWM Kit is designed for easy installation, making it suitable for both novice users and experienced PC builders. The fans come with standard mounting holes and include all necessary hardware, allowing for hassle-free installation in any compatible case.</p>
                <h2>Versatile Compatibility</h2>
                <p>Compatible with a wide range of PC cases and cooling configurations, the Silver Monkey X Sirocco 3x120 mm PWM Kit offers versatile compatibility to suit your needs. Whether youre building a gaming rig, a workstation, or a home theater PC, this kit provides the cooling performance you need for optimal system stability.</p>
                <h2>RGB Lighting Option</h2>
                <p>For users looking to add a touch of style to their build, the Silver Monkey X Sirocco 3x120 mm PWM Kit is also available with RGB lighting options. Choose from a variety of vibrant colors and effects to customize the look of your PC and create a stunning visual display.</p>
                <h2>Upgrade Your Cooling</h2>
                <p>Upgrade your PCs cooling system with the Silver Monkey X Sirocco 3x120 mm PWM Kit and enjoy improved performance, reliability, and aesthetics. Whether youre overclocking your CPU, gaming for hours on end, or running demanding applications, this kit ensures that your system stays cool and stable under pressure.</p>""",
            "sale_id": None,
            },
            {
            "id": 49,
            "name": "Silver Monkey X Oroshi 120 mm PWM ARGB WHT",
            "price": 10.0,
            "old_price": 15.0,
            "description": """<h2>Dynamic Cooling with ARGB Lighting</h2>
                <p>Elevate your PC cooling setup with the Silver Monkey X Oroshi 120 mm PWM ARGB WHT fan. Combining powerful cooling performance with mesmerizing ARGB lighting, this fan is designed to enhance both the aesthetics and functionality of your system.</p>
                <h2>Efficient Cooling Performance</h2>
                <p>The Oroshi 120 mm fan features a high-quality PWM motor that delivers efficient cooling performance while maintaining low noise levels. Whether youre gaming, overclocking, or running demanding applications, this fan ensures optimal airflow to keep your components cool and stable.</p>
                <h2>Customizable ARGB Lighting</h2>
                <p>Add a splash of color to your build with the customizable ARGB lighting of the Oroshi fan. With a wide range of vibrant colors and dynamic lighting effects to choose from, you can create stunning visual displays that match your style and preferences.</p>
                <h2>Quiet Operation</h2>
                <p>Enjoy a quiet computing experience thanks to the advanced PWM control of the Oroshi fan. By dynamically adjusting the fan speed based on temperature, it effectively cools your system while keeping noise to a minimum, even under heavy loads.</p>
                <h2>Easy Installation</h2>
                <p>The Oroshi 120 mm fan is designed for easy installation in any standard case. With its universal 120 mm size and standard mounting holes, it seamlessly integrates into your existing setup without any hassle.</p>
                <h2>Enhance Your Build</h2>
                <p>Upgrade your PC cooling solution with the Silver Monkey X Oroshi 120 mm PWM ARGB WHT fan and experience a perfect balance of performance and aesthetics. Whether youre building a gaming rig, a workstation, or a multimedia PC, this fan adds flair and functionality to any setup.</p>""",
            "sale_id": None,
            },
            {
            "id": 50,
            "name": "be quiet! Silent Wings 4 120mm PWM",
            "price": 15.0,
            "old_price": 35.0,
            "description": """<h2>Silent and Efficient Cooling</h2>
                <p>Experience exceptional cooling performance with the be quiet! Silent Wings 4 120mm PWM fan. Engineered for whisper-quiet operation, this fan delivers superior airflow while maintaining near-silent noise levels, making it perfect for high-performance systems.</p>
                <h2>Advanced PWM Control</h2>
                <p>Equipped with advanced PWM control, the Silent Wings 4 fan allows for precise speed adjustments, ensuring optimal cooling performance under varying load conditions. Whether youre gaming, editing, or simply browsing the web, this fan adapts to your systems needs.</p>
                <h2>Unique Fan Blade Design</h2>
                <p>The Silent Wings 4 features a unique fan blade design optimized for maximum airflow and minimal noise generation. Its innovative design reduces turbulence and improves air circulation, resulting in efficient cooling without the distracting noise.</p>
                <h2>Anti-Vibration Mounting</h2>
                <p>Reduce vibrations and noise even further with the be quiet! Silent Wings 4s anti-vibration mounting system. The fan is equipped with rubberized mounting pads that absorb vibrations and minimize noise transmission, ensuring a quiet computing experience.</p>
                <h2>Long-Lasting Reliability</h2>
                <p>Backed by be quiet!s renowned quality and reliability, the Silent Wings 4 fan is built to last. With high-quality components and rigorous testing, this fan delivers reliable performance day in and day out, ensuring your system stays cool and quiet for years to come.</p>
                <h2>Easy Installation</h2>
                <p>Installing the be quiet! Silent Wings 4 fan is quick and hassle-free. With its standard 120mm size and compatible mounting holes, it fits seamlessly into most PC cases and cooling setups, allowing you to upgrade your system with ease.</p>
                <h2>Enhance Your PC Experience</h2>
                <p>Upgrade your PC cooling solution with the be quiet! Silent Wings 4 120mm PWM fan and enjoy silent and efficient cooling performance. Whether youre a gamer, content creator, or power user, this fan delivers the perfect balance of silence, performance, and reliability.</p>""",
            "sale_id": 5,
            },
            {
            "id": 51,
            "name": "Fractal Design Prisma AL-12 ARGB PWM 120mm",
            "price": 15.0,
            "old_price": 25.0,
            "description": """<h2>Illuminate Your Build with ARGB Lighting</h2>
                <p>Elevate your PCs aesthetics with the Fractal Design Prisma AL-12 ARGB PWM 120mm fan. Featuring addressable RGB (ARGB) lighting, this fan adds vibrant and customizable lighting effects to your build, creating a stunning visual centerpiece.</p>
                <h2>Efficient Cooling Performance</h2>
                <p>Experience powerful cooling performance with the Prisma AL-12 fan. Designed with high-quality components and optimized fan blades, it delivers efficient airflow to effectively dissipate heat from your components, ensuring stable and reliable operation.</p>
                <h2>Advanced PWM Control</h2>
                <p>Enjoy precise control over fan speed and noise levels with the Prisma AL-12s PWM (Pulse Width Modulation) support. Adjust the fan speed dynamically based on your systems temperature requirements, striking the perfect balance between cooling performance and noise levels.</p>
                <h2>Customizable ARGB Effects</h2>
                <p>Express your style and personality with customizable ARGB lighting effects. The Prisma AL-12 fan allows you to choose from a wide range of lighting presets and colors, or sync the lighting with compatible ARGB components and peripherals for a synchronized lighting experience.</p>
                <h2>Low-Noise Operation</h2>
                <p>Experience whisper-quiet operation with the Prisma AL-12 fans advanced PWM control and optimized fan blade design. Enjoy efficient cooling without sacrificing silence, making it ideal for noise-sensitive environments or those who prefer a quieter computing experience.</p>
                <h2>Easy Installation and Compatibility</h2>
                <p>The Prisma AL-12 fan features a standard 120mm form factor and comes with mounting screws for easy installation in most PC cases and cooling configurations. Its compatibility with popular motherboard RGB software allows for seamless integration and control.</p>
                <h2>Enhance Your Build</h2>
                <p>Upgrade your PCs cooling and aesthetics with the Fractal Design Prisma AL-12 ARGB PWM 120mm fan. With its stunning ARGB lighting, efficient cooling performance, and customizable features, its the perfect choice for gamers, enthusiasts, and anyone looking to elevate their PC build.</p>""",
            "sale_id": None,
            },
            {
                "id": 52,
                "name": "Fractal Design Aspect 14 RGB Black Frame 140mm",
                "price": 10.0,
                "old_price": 15.0,
                "description": """<h2>Elevate Your Systems Aesthetics with RGB Lighting</h2>
                <p>Add a touch of style and vibrancy to your PC build with the Fractal Design Aspect 14 RGB fan. Featuring a sleek black frame and customizable RGB lighting, this 140mm fan enhances the visual appeal of your system while providing efficient cooling performance.</p>
                <h2>Customizable RGB Lighting Effects</h2>
                <p>Express your creativity and personalize your build with the Aspect 14 RGB fans customizable RGB lighting effects. Choose from a spectrum of colors and dynamic lighting patterns to match your setup or create a unique lighting display that reflects your style.</p>
                <h2>Optimized Cooling Performance</h2>
                <p>Designed for efficient airflow and cooling, the Aspect 14 RGB fan delivers reliable performance to keep your components running smoothly. Its optimized blade design and high-quality bearings ensure effective heat dissipation without compromising on noise levels.</p>
                <h2>Quiet Operation</h2>
                <p>Enjoy a quieter computing experience with the Aspect 14 RGB fans low-noise operation. With advanced motor technology and vibration-dampening features, this fan minimizes noise while maximizing airflow, making it ideal for noise-sensitive environments or those who prefer a quieter PC.</p>
                <h2>Easy Installation and Compatibility</h2>
                <p>The Aspect 14 RGB fan features a standard 140mm size and comes with mounting screws for easy installation in most PC cases and cooling setups. Its compatibility with popular motherboard RGB software allows for seamless integration and control, making customization effortless.</p>
                <h2>Enhance Your Build with Style and Performance</h2>
                <p>Elevate your PC build with the Fractal Design Aspect 14 RGB fan. Combining stylish design with efficient cooling performance and customizable RGB lighting, its the perfect choice for enthusiasts and gamers looking to enhance their system aesthetics while maintaining optimal airflow.</p>""",
                "sale_id": None,
            },
            {
                "id": 53,
                "name": "Corsair iCUE LINK QX120 PWM RGB White 120mm",
                "price": 30.0,
                "old_price": 45.0,
                "description": """<h2>Elevate Your PC Aesthetics with Customizable RGB Lighting</h2>
                <p>Transform the look of your PC with the Corsair iCUE LINK QX120 PWM RGB fan. Featuring a sleek white design and customizable RGB lighting, this 120mm fan adds vibrant illumination to your system while delivering powerful cooling performance.</p>
                <h2>Customizable RGB Lighting Effects</h2>
                <p>Express your creativity and personalize your build with the iCUE LINK QX120 PWM RGB fans customizable RGB lighting effects. Choose from a wide range of colors and dynamic lighting patterns using Corsairs iCUE software to match your setup or create stunning visual effects that reflect your style.</p>
                <h2>Efficient Cooling Performance</h2>
                <p>Designed for optimal airflow and cooling efficiency, the iCUE LINK QX120 PWM RGB fan ensures reliable performance to keep your components running cool under heavy loads. Its high-quality fan blades and advanced motor technology deliver exceptional airflow while minimizing noise levels, making it suitable for both gaming and demanding workloads.</p>
                <h2>Integrated Corsair iCUE Software</h2>
                <p>Take full control of your RGB lighting and fan speed settings with Corsairs iCUE software. Customize lighting effects, adjust fan speeds, and synchronize your fan lighting with other compatible Corsair RGB products for a cohesive and immersive lighting experience across your entire system.</p>
                <h2>Quiet Operation</h2>
                <p>Enjoy a quieter computing experience with the iCUE LINK QX120 PWM RGB fans low-noise operation. Designed with noise-reducing features and optimized fan blade design, it maintains quiet performance even at high speeds, allowing you to focus on your tasks without distraction.</p>
                <h2>Easy Installation and Compatibility</h2>
                <p>The iCUE LINK QX120 PWM RGB fan features a standard 120mm size and comes with mounting screws for easy installation in most PC cases and cooling setups. Its compatibility with Corsairs iCUE ecosystem ensures seamless integration and control, making it effortless to customize your lighting and fan settings.</p>
                <h2>Enhance Your PC Build with Style and Performance</h2>
                <p>Upgrade your PC build with the Corsair iCUE LINK QX120 PWM RGB fan. Combining stylish design with customizable RGB lighting and efficient cooling performance, its the perfect choice for enthusiasts and gamers who want to elevate their system aesthetics while maintaining optimal airflow and temperature control.</p>""",
                "sale_id": None,
            },
            {
                "id": 54,
                "name": "Corsair LL120 RGB LED Static PWM Triple Pack 3x120mm",
                "price": 130.0,
                "old_price": 145.0,
                "description": """<h2>Elevate Your PC Aesthetics with Vibrant RGB Lighting</h2>
                <p>Upgrade your PCs visual appeal with the Corsair LL120 RGB LED Static PWM Triple Pack. Featuring three 120mm fans with customizable RGB lighting, this pack adds vibrant colors and dynamic effects to your system, enhancing its overall look and feel.</p>
                <h2>Customizable RGB Lighting Effects</h2>
                <p>Express your creativity and personalize your PCs lighting with the LL120 RGB LED fans. Choose from a wide range of colors and dynamic lighting effects using Corsairs iCUE software, allowing you to match your setups theme or create eye-catching visual displays.</p>
                <h2>Efficient Cooling Performance</h2>
                <p>Besides delivering stunning RGB lighting, the LL120 RGB LED fans provide excellent cooling performance to keep your system running smoothly. With optimized fan blades and PWM control, they offer efficient airflow while maintaining low noise levels, ensuring effective cooling without sacrificing silence.</p>
                <h2>Dynamic Lighting Synchronization</h2>
                <p>Synchronize the RGB lighting of your LL120 fans with other compatible Corsair RGB products using Corsairs iCUE software. Create immersive lighting effects that flow seamlessly across your entire setup, enhancing the visual impact of your gaming or workstation environment.</p>
                <h2>Quiet Operation</h2>
                <p>Enjoy a quieter computing experience with the LL120 RGB LED fans low-noise operation. Designed with noise-reducing features and advanced motor technology, they deliver impressive cooling performance while minimizing noise, allowing you to focus on your tasks without distraction.</p>
                <h2>Easy Installation and Compatibility</h2>
                <p>The LL120 RGB LED fans come in a triple pack with mounting screws included for easy installation in most PC cases and cooling configurations. Their standard 120mm size ensures compatibility with a wide range of setups, while their integration with Corsairs iCUE ecosystem makes customization and control effortless.</p>
                <h2>Elevate Your PC Build with Stunning RGB Lighting</h2>
                <p>Upgrade your PC build with the Corsair LL120 RGB LED Static PWM Triple Pack. With customizable RGB lighting, efficient cooling performance, and quiet operation, these fans are the perfect choice for enthusiasts and gamers who want to take their system aesthetics to the next level.</p>""",
                "sale_id": None,
            },
            {
                "id": 55,
                "name": "Corsair iCUE QL120 RGB PWM Triple Pack+Lighting Node 3x120",
                "price": 150.0,
                "old_price": 155.0,
                "description": """<h2>Elevate Your PC Aesthetics with Stunning RGB Lighting</h2>
                <p>Enhance the visual appeal of your PC build with the Corsair iCUE QL120 RGB PWM Triple Pack. Featuring three 120mm fans equipped with vibrant RGB lighting and a Lighting Node CORE controller, this pack offers a captivating lighting experience that brings your system to life.</p>
                <h2>Immersive RGB Lighting Effects</h2>
                <p>Express your creativity and personalize your PCs lighting with the QL120 RGB PWM fans. With 34 individually addressable RGB LEDs per fan, you can create mesmerizing lighting effects and dynamic color patterns using Corsairs powerful iCUE software. Choose from a wide range of colors and effects to match your setups theme or create stunning visual displays.</p>
                <h2>Efficient Cooling Performance</h2>
                <p>Besides delivering striking RGB lighting, the QL120 RGB PWM fans provide excellent cooling performance to keep your system running optimally. Featuring a specially designed fan blade and PWM control, they offer efficient airflow while maintaining low noise levels, ensuring effective cooling without compromising on silence.</p>
                <h2>Integrated Lighting Node CORE Controller</h2>
                <p>The included Lighting Node CORE controller allows seamless synchronization of your QL120 RGB PWM fans lighting effects. Connect the fans to the controller and customize their lighting using Corsairs iCUE software, enabling dynamic lighting synchronization across your entire setup for a cohesive and immersive experience.</p>
                <h2>Quiet Operation</h2>
                <p>Enjoy a quieter computing experience with the QL120 RGB PWM fans low-noise operation. Designed with noise-reducing features and advanced motor technology, they deliver impressive cooling performance while minimizing noise, allowing you to focus on your tasks without distraction.</p>
                <h2>Easy Installation and Compatibility</h2>
                <p>The QL120 RGB PWM fans come in a triple pack with mounting screws included for easy installation in most PC cases and cooling configurations. Their standard 120mm size ensures compatibility with a wide range of setups, while their integration with Corsairs iCUE ecosystem makes customization and control effortless.</p>
                <h2>Elevate Your PC Build with Mesmerizing RGB Lighting</h2>
                <p>Transform your PC build with the Corsair iCUE QL120 RGB PWM Triple Pack+Lighting Node. Featuring captivating RGB lighting, efficient cooling performance, and quiet operation, these fans are the perfect choice for enthusiasts and gamers who demand both style and substance in their systems.</p>""",
                "sale_id": None,
            },
            {
                "id": 56,
                "name": "Corsair LL120 RGB White Triple Pack+Node PRO 3x120mm",
                "price": 125.0,
                "old_price": 135.0,
                "description": """<h2>Elevate Your PC Aesthetics with Brilliant RGB Lighting</h2>
                <p>Upgrade your PCs visual appeal with the Corsair LL120 RGB White Triple Pack. Featuring three 120mm fans with stunning RGB lighting and a Node PRO controller, this pack offers an immersive lighting experience that transforms your system into a visual masterpiece.</p>
                <h2>Immersive RGB Lighting Effects</h2>
                <p>Express your creativity and customize your PCs lighting with the LL120 RGB White fans. Equipped with 16 individually addressable RGB LEDs per fan, you can create captivating lighting effects and dynamic color patterns using Corsairs powerful iCUE software. Choose from a wide range of colors and effects to match your setups theme or create mesmerizing visual displays.</p>
                <h2>Efficient Cooling Performance</h2>
                <p>Besides delivering stunning RGB lighting, the LL120 RGB White fans provide excellent cooling performance to keep your system running smoothly. Featuring specially designed fan blades and PWM control, they offer efficient airflow while maintaining low noise levels, ensuring effective cooling without compromising on silence.</p>
                <h2>Integrated Node PRO Controller</h2>
                <p>The included Node PRO controller enables seamless synchronization of your LL120 RGB White fans lighting effects. Connect the fans to the controller and customize their lighting using Corsairs iCUE software, allowing for dynamic lighting synchronization across your entire setup for a cohesive and immersive experience.</p>
                <h2>Quiet Operation</h2>
                <p>Enjoy a quieter computing experience with the LL120 RGB White fans low-noise operation. Designed with noise-reducing features and advanced motor technology, they deliver impressive cooling performance while minimizing noise, allowing you to focus on your tasks without distraction.</p>
                <h2>Easy Installation and Compatibility</h2>
                <p>The LL120 RGB White fans come in a triple pack with mounting screws included for easy installation in most PC cases and cooling configurations. Their standard 120mm size ensures compatibility with a wide range of setups, while their integration with Corsairs iCUE ecosystem makes customization and control effortless.</p>
                <h2>Elevate Your PC Build with Brilliant RGB Lighting</h2>
                <p>Transform your PC build with the Corsair LL120 RGB White Triple Pack+Node PRO. Featuring stunning RGB lighting, efficient cooling performance, and quiet operation, these fans are the perfect choice for enthusiasts and gamers who demand both style and substance in their systems.</p>""",
                "sale_id": None,
            },
            {
                "id": 57,
                "name": "Gigabyte GeForce RTX 4060 Eagle OC 8GB GDDR6",
                "price": 350.0,
                "old_price": 445.0,
                "description": """<h2>Immersive Gaming Performance with Gigabyte</h2>
                <p>Elevate your gaming experience with the Gigabyte GeForce RTX 4060 Eagle OC graphics card. Powered by NVIDIAs Ampere architecture and featuring 8GB of GDDR6 memory, this GPU delivers exceptional performance, stunning visuals, and advanced gaming features for immersive gameplay.</p>
                <h2>Powerful Ampere Architecture</h2>
                <p>Experience the power of NVIDIAs Ampere architecture, which provides a significant leap in performance and efficiency compared to previous generations. With enhanced CUDA cores, RT cores for ray tracing, and Tensor cores for AI acceleration, the RTX 4060 Eagle OC delivers unparalleled gaming performance and realism.</p>
                <h2>High-Speed GDDR6 Memory</h2>
                <p>Equipped with 8GB of GDDR6 memory, the RTX 4060 Eagle OC ensures smooth and responsive gameplay, even at high resolutions and detail settings. The high-speed memory bandwidth allows for faster data transfer, reducing latency and ensuring a seamless gaming experience.</p>
                <h2>Boosted Clock Speeds for Enhanced Performance</h2>
                <p>The Eagle OC variant of the RTX 4060 comes with factory overclocked settings, providing higher boost clock speeds out of the box for increased performance in demanding games and applications. Enjoy faster frame rates and smoother gameplay without compromising stability.</p>
                <h2>Advanced Cooling for Optimal Performance</h2>
                <p>Gigabytes WindForce 3X cooling system features triple fans with alternate spinning, direct-touch copper heat pipes, and a unique blade design to efficiently dissipate heat and keep the GPU cool under heavy load. This ensures stable performance and extends the lifespan of the graphics card.</p>
                <h2>RGB Fusion 2.0 Lighting</h2>
                <p>Customize the look of your gaming rig with Gigabytes RGB Fusion 2.0 lighting system. The RTX 4060 Eagle OC features customizable RGB lighting on the shroud, allowing you to synchronize colors and effects with other RGB components for a cohesive and visually stunning setup.</p>
                <h2>Comprehensive Connectivity Options</h2>
                <p>The RTX 4060 Eagle OC offers a range of connectivity options, including multiple DisplayPort 1.4a and HDMI 2.1 ports, allowing you to connect up to four displays for immersive gaming and multitasking. The card also features PCIe 4.0 support for high-speed data transfer.</p>
                <h2>Software Suite for Performance Optimization</h2>
                <p>Gigabytes Aorus Engine software allows you to monitor and tweak various settings of your RTX 4060 Eagle OC graphics card, including clock speeds, fan profiles, and RGB lighting effects. Maximize performance and customize your gaming experience with intuitive software control.</p>
                <h2>Experience Next-Generation Gaming</h2>
                <p>With its powerful performance, advanced features, and sleek design, the Gigabyte GeForce RTX 4060 Eagle OC 8GB GDDR6 graphics card is the perfect choice for gamers and enthusiasts looking to take their gaming experience to the next level. Immerse yourself in stunning visuals and seamless gameplay with Gigabytes latest GPU offering.</p>""",
                "sale_id": None,
            },
            {
                "id": 58,
                "name": "MSI GeForce RTX 4060 Ti Gaming X SLIM 16GB GDDR6",
                "price": 400.0,
                "old_price": 455.0,
                "description": """<h2>Elevate Your Gaming Experience with MSI</h2>
                <p>Experience unparalleled gaming performance with the MSI GeForce RTX 4060 Ti Gaming X SLIM graphics card. Built on NVIDIAs Ampere architecture and featuring 16GB of GDDR6 memory, this GPU delivers exceptional power and efficiency for immersive gaming experiences.</p>
                <h2>Advanced Ampere Architecture</h2>
                <p>Powered by NVIDIAs Ampere architecture, the RTX 4060 Ti Gaming X SLIM delivers incredible gaming performance and realistic graphics. With dedicated RT cores for ray tracing and Tensor cores for AI acceleration, youll experience lifelike visuals and smooth gameplay in the latest titles.</p>
                <h2>High-Speed GDDR6 Memory</h2>
                <p>Equipped with 16GB of high-speed GDDR6 memory, the RTX 4060 Ti Gaming X SLIM ensures lightning-fast data transfer and responsive gaming performance. Enjoy smooth frame rates and quick load times, even at high resolutions and detail settings.</p>
                <h2>Boost Clock Technology for Enhanced Performance</h2>
                <p>Featuring MSIs exclusive Boost Clock technology, the RTX 4060 Ti Gaming X SLIM delivers higher clock speeds for increased performance in demanding games and applications. Unlock the full potential of your GPU and enjoy smoother gaming experiences.</p>
                <h2>Efficient Cooling Design</h2>
                <p>The Gaming X SLIM variant of the RTX 4060 Ti features MSIs advanced cooling solution, ensuring optimal thermal performance even under heavy load. The TORX FAN 4.0 technology combines dispersion fan blades and traditional fan blades to generate concentrated airflow and enhance cooling efficiency.</p>
                <h2>RGB Mystic Light Integration</h2>
                <p>Customize the look of your gaming rig with MSIs RGB Mystic Light technology. The RTX 4060 Ti Gaming X SLIM features customizable RGB lighting on the shroud, allowing you to personalize your setup with vibrant colors and dynamic effects that synchronize with other Mystic Light-compatible components.</p>
                <h2>Zero Frozr Technology for Silent Operation</h2>
                <p>MSIs Zero Frozr technology ensures silent operation during low-load sPRICErios by stopping the fans when temperatures are below a certain threshold. This allows for quieter gaming sessions and reduces unnecessary noise in your gaming environment.</p>
                <h2>Comprehensive Connectivity Options</h2>
                <p>The RTX 4060 Ti Gaming X SLIM offers a variety of connectivity options, including multiple DisplayPort 1.4a and HDMI 2.1 ports, enabling seamless connectivity with the latest display technologies. Connect multiple monitors for immersive gaming experiences or productivity multitasking.</p>
                <h2>MSI Dragon Center Software</h2>
                <p>Take control of your gaming experience with the MSI Dragon Center software. Monitor your GPUs performance, adjust fan speeds, customize RGB lighting effects, and optimize game settings all from one intuitive interface. Maximize your gaming potential with MSIs powerful software suite.</p>
                <h2>Immersive Gaming Performance</h2>
                <p>With its powerful performance, innovative features, and sleek design, the MSI GeForce RTX 4060 Ti Gaming X SLIM 16GB GDDR6 graphics card delivers unmatched gaming experiences. Elevate your gameplay to new heights and immerse yourself in the latest AAA titles with MSIs cutting-edge GPU technology.</p>""",
                "sale_id": None,
            },
            {
                "id": 59,
                "name": "Gigabyte GeForce RTX 3060 GAMING OC LHR 12GB GDDR6",
                "price": 300.0,
                "old_price": 335.0,
                "description": """<h2>Elevate Your Gaming Experience with Gigabyte</h2>
                <p>Experience exceptional gaming performance and lifelike graphics with the Gigabyte GeForce RTX 3060 GAMING OC LHR graphics card. Featuring 12GB of GDDR6 memory and advanced cooling technology, this GPU is designed to deliver smooth gameplay and immersive visuals for todays most demanding titles.</p>
                <h2>Powered by NVIDIA Ampere Architecture</h2>
                <p>Powered by NVIDIAs Ampere architecture, the RTX 3060 GAMING OC LHR delivers incredible gaming performance and realism. With dedicated RT cores for ray tracing and Tensor cores for AI processing, you can enjoy realistic lighting, shadows, and reflections in your favorite games.</p>
                <h2>12GB GDDR6 Memory</h2>
                <p>Equipped with 12GB of high-speed GDDR6 memory, the RTX 3060 GAMING OC LHR ensures smooth performance and responsiveness, even in the most demanding gaming sPRICErios. Experience faster load times, smoother frame rates, and seamless gameplay with ample memory capacity.</p>
                <h2>Advanced Cooling Technology</h2>
                <p>The GAMING OC variant of the RTX 3060 features Gigabytes advanced cooling solution, designed to keep temperatures in check during intense gaming sessions. The WindForce 3X cooling system combines three unique blade fans with alternate spinning to maximize airflow and heat dissipation.</p>
                <h2>RGB Fusion 2.0</h2>
                <p>Customize the look of your gaming rig with Gigabytes RGB Fusion 2.0 lighting technology. The RTX 3060 GAMING OC LHR features customizable RGB lighting on the shroud, allowing you to personalize your setup with vibrant colors and dynamic effects that synchronize with other RGB Fusion-compatible components.</p>
                <h2>Efficient Power Delivery</h2>
                <p>The RTX 3060 GAMING OC LHR features an efficient power delivery system, ensuring stable and reliable performance under heavy load. With Gigabytes Ultra Durable components and enhanced circuit design, this GPU delivers consistent power delivery for optimal gaming performance.</p>
                <h2>Multiple Display Connectivity</h2>
                <p>Connectivity options on the RTX 3060 GAMING OC LHR include multiple DisplayPort 1.4a and HDMI 2.1 ports, allowing for seamless connectivity with the latest display technologies. Enjoy high-resolution gaming on multiple monitors or immersive VR experiences with ease.</p>
                <h2>Intuitive AORUS Engine Software</h2>
                <p>Take control of your gaming experience with the Gigabyte AORUS Engine software. Monitor your GPUs performance, adjust fan speeds, customize RGB lighting effects, and optimize game settings all from one intuitive interface. Maximize your gaming potential with Gigabytes powerful software suite.</p>
                <h2>Immersive Gaming Performance</h2>
                <p>With its powerful performance, innovative features, and sleek design, the Gigabyte GeForce RTX 3060 GAMING OC LHR 12GB GDDR6 graphics card delivers unmatched gaming experiences. Elevate your gameplay to new heights and immerse yourself in the latest AAA titles with Gigabytes cutting-edge GPU technology.</p>""",
                "sale_id": None,
            },
            {
                "id": 60,
                "name": "Gigabyte Radeon RX 6600 EAGLE 8GB GDDR6",
                "price": 200.0,
                "old_price": 235.0,
                "description": """<h2>Unleash Your Gaming Potential with Gigabyte</h2>
                <p>Experience high-performance gaming with the Gigabyte Radeon RX 6600 EAGLE 8GB GDDR6 graphics card. Designed to deliver exceptional visuals and smooth gameplay, this GPU is perfect for both casual gamers and esports enthusiasts.</p>
                <h2>Powerful Graphics Performance</h2>
                <p>The Radeon RX 6600 EAGLE is equipped with 8GB of GDDR6 memory and features AMDs RDNA 2 architecture, delivering stunning graphics and responsive gameplay. With support for the latest DirectX 12 Ultimate features, you can enjoy lifelike visuals and immersive gaming experiences.</p>
                <h2>Advanced Cooling Technology</h2>
                <p>Featuring Gigabytes WINDFORCE 3X cooling system, the RX 6600 EAGLE ensures optimal thermal performance even during intense gaming sessions. The triple-fan design and direct-touch heat pipes help dissipate heat efficiently, keeping temperatures low and performance high.</p>
                <h2>Efficient Power Delivery</h2>
                <p>With its advanced power delivery system, the RX 6600 EAGLE delivers reliable performance while minimizing power consumption. Gigabytes Ultra Durable components ensure stability and longevity, allowing you to game with confidence for hours on end.</p>
                <h2>Customizable RGB Lighting</h2>
                <p>Enhance your gaming setup with customizable RGB lighting on the RX 6600 EAGLE. With Gigabytes RGB Fusion 2.0 technology, you can personalize the lighting effects to match your style or synchronize them with other RGB-enabled components for a cohesive look.</p>
                <h2>Intuitive Software Controls</h2>
                <p>Take control of your gaming experience with Gigabytes intuitive software suite. The Radeon RX 6600 EAGLE is compatible with the AORUS Engine software, allowing you to monitor performance metrics, adjust fan speeds, and customize RGB lighting with ease.</p>
                <h2>Multiple Display Connectivity</h2>
                <p>Connectivity options on the RX 6600 EAGLE include multiple DisplayPort 1.4 and HDMI 2.1 ports, allowing you to easily connect to a variety of monitors and display devices. Whether youre gaming on a high-refresh-rate monitor or enjoying immersive VR experiences, the RX 6600 EAGLE has you covered.</p>
                <h2>Immersive Gaming Experience</h2>
                <p>Whether youre exploring vast open worlds or competing in fast-paced multiplayer battles, the Gigabyte Radeon RX 6600 EAGLE 8GB GDDR6 graphics card delivers the performance and reliability you need to dominate the competition. Elevate your gaming experience with Gigabytes cutting-edge GPU technology.</p>""",
                "sale_id": None,
            },
            {
                "id": 61,
                "name": "MSI GeForce RTX 4060 Ti Ventus 2X Black OC 16GB GDDR6",
                "price": 325.0,
                "old_price": 335.0,
                "description": """<h2>Elevate Your Gaming Experience with MSI</h2>
                    <p>Experience the pinnacle of gaming performance with the MSI GeForce RTX 4060 Ti Ventus 2X Black OC graphics card. Built on NVIDIAs Ampere architecture and equipped with 16GB of GDDR6 memory, this GPU delivers unparalleled gaming power and immersion for both casual and hardcore gamers alike.</p>
                    <h2>Powerful Graphics Processing</h2>
                    <p>The GeForce RTX 4060 Ti Ventus 2X Black OC features NVIDIAs latest Ampere architecture, offering a significant boost in gaming performance and ray tracing capabilities. With 16GB of GDDR6 memory, you can enjoy smooth gameplay and stunning visuals in the latest AAA titles.</p>
                    <h2>Efficient Cooling Design</h2>
                    <p>Equipped with MSIs award-winning Ventus 2X cooling solution, this graphics card ensures optimal thermal performance even under heavy load. The dual-fan design and advanced heatsink keep temperatures low, allowing you to push your GPU to its limits without compromising performance.</p>
                    <h2>Overclocking Capabilities</h2>
                    <p>With MSIs exclusive Afterburner software, you can easily overclock your RTX 4060 Ti Ventus 2X Black OC for even greater gaming performance. Unlock the full potential of your GPU and experience smoother gameplay and faster frame rates in your favorite games.</p>
                    <h2>Immersive Ray Tracing</h2>
                    <p>Thanks to its dedicated ray tracing cores, the RTX 4060 Ti Ventus 2X Black OC delivers stunning visuals and lifelike lighting effects in supported games. Experience realistic reflections, shadows, and ambient occlusion for a truly immersive gaming experience.</p>
                    <h2>Advanced Connectivity</h2>
                    <p>Connectivity options on the RTX 4060 Ti Ventus 2X Black OC include DisplayPort 1.4a and HDMI 2.1 ports, allowing you to easily connect to high-resolution monitors and VR headsets. Enjoy smooth, tear-free gaming at high refresh rates and resolutions up to 4K.</p>
                    <h2>RGB Lighting Effects</h2>
                    <p>Add a touch of style to your gaming rig with customizable RGB lighting on the RTX 4060 Ti Ventus 2X Black OC. With MSIs Mystic Light software, you can personalize the lighting effects to match your setup and create a visually stunning gaming environment.</p>
                    <h2>Enhanced Durability</h2>
                    <p>MSIs Military Class components ensure long-term reliability and stability, even under demanding gaming conditions. With a solid build quality and rigorous testing procedures, you can trust the RTX 4060 Ti Ventus 2X Black OC to deliver consistent performance for years to come.</p>
                    <h2>Experience Gaming at Its Best</h2>
                    <p>Whether youre exploring vast open worlds, competing in esports tournaments, or diving into virtual reality experiences, the MSI GeForce RTX 4060 Ti Ventus 2X Black OC 16GB GDDR6 graphics card delivers the performance and reliability you need to dominate the competition. Elevate your gaming experience with MSIs industry-leading GPU technology.</p>""",
                "sale_id": None,
            },
            {
                "id": 62,
                "name": "Gigabyte GeForce RTX 4070 SUPER WINDFORCE OC 12GB GDDR6X",
                "price": 625.0,
                "old_price": 635.0,
                "description": """<h2>Unleash Gaming Performance with Gigabyte</h2>
                <p>Experience unparalleled gaming performance with the Gigabyte GeForce RTX 4070 SUPER WINDFORCE OC graphics card. Engineered for maximum power and efficiency, this GPU is equipped with 12GB of GDDR6X memory and features Gigabytes renowned WINDFORCE cooling solution for superior thermal performance.</p>
                <h2>Next-Gen Graphics Processing</h2>
                <p>The GeForce RTX 4070 SUPER WINDFORCE OC is powered by NVIDIAs cutting-edge Ampere architecture, delivering incredible gaming performance and advanced ray tracing capabilities. With 12GB of ultra-fast GDDR6X memory, you can enjoy smooth gameplay and stunning visuals in the latest AAA titles.</p>
                <h2>Efficient Cooling Design</h2>
                <p>Equipped with Gigabytes WINDFORCE cooling system, this graphics card ensures optimal thermal performance under heavy gaming loads. The triple-fan design and large heatsink effectively dissipate heat, allowing you to push your GPU to its limits without worrying about overheating.</p>
                <h2>Overclocking Ready</h2>
                <p>Unlock the full potential of your GPU with Gigabytes intuitive AORUS Engine software. Easily overclock your RTX 4070 SUPER WINDFORCE OC for even greater gaming performance and enjoy faster frame rates and smoother gameplay in your favorite games.</p>
                <h2>Immersive Ray Tracing</h2>
                <p>Experience lifelike graphics and stunning visual effects with real-time ray tracing technology. The RTX 4070 SUPER WINDFORCE OC features dedicated ray tracing cores for realistic reflections, shadows, and lighting effects, bringing your games to life like never before.</p>
                <h2>Advanced Connectivity</h2>
                <p>Connectivity options on the RTX 4070 SUPER WINDFORCE OC include DisplayPort 1.4a and HDMI 2.1 ports, allowing you to easily connect to high-resolution monitors and VR headsets. Enjoy smooth, tear-free gaming at high refresh rates and resolutions up to 8K.</p>
                <h2>RGB Fusion 2.0</h2>
                <p>Customize your gaming rig with Gigabytes RGB Fusion 2.0 software. Choose from a variety of lighting effects and colors to match your setup and create a unique gaming aesthetic. Sync your RGB lighting with other compatible Gigabyte components for a cohesive look.</p>
                <h2>Enhanced Durability</h2>
                <p>Gigabytes Ultra Durable components ensure long-term reliability and stability, even under extreme gaming conditions. With a robust build quality and rigorous testing procedures, you can trust the RTX 4070 SUPER WINDFORCE OC to deliver consistent performance for years to come.</p>
                <h2>Elevate Your Gaming Experience</h2>
                <p>Whether youre exploring vast open worlds, competing in esports tournaments, or diving into virtual reality experiences, the Gigabyte GeForce RTX 4070 SUPER WINDFORCE OC 12GB GDDR6X graphics card delivers the performance and reliability you need to dominate the competition. Experience gaming at its best with Gigabytes industry-leading GPU technology.</p>""",
                "sale_id": None,
            },
            {
                "id": 63,
                "name": "MSI GeForce RTX 4070 Ti SUPER VENTUS 2X OC 16GB GDDR6X",
                "price": 725.0,
                "old_price": 735.0,
                "description": """<h2>Unleash Next-Generation Gaming</h2>
                <p>Experience the ultimate in gaming performance with the MSI GeForce RTX 4070 Ti SUPER VENTUS 2X OC graphics card. Powered by NVIDIAs Ampere architecture and featuring 16GB of GDDR6X memory, this GPU delivers unrivaled graphics performance for the most demanding games and applications.</p>
                <h2>Advanced Cooling Technology</h2>
                <p>The RTX 4070 Ti SUPER VENTUS 2X OC is equipped with MSIs TORX Fan 4.0 cooling system, featuring two high-performance fans with advanced aerodynamics. Combined with a large heatsink and heat pipes, this cooling solution ensures efficient heat dissipation and keeps your GPU running cool even under heavy loads.</p>
                <h2>Boosted Performance</h2>
                <p>With factory overclocked speeds and MSIs exclusive Afterburner overclocking utility, you can push your RTX 4070 Ti SUPER VENTUS 2X OC even further for increased performance. Unlock higher frame rates and smoother gameplay in your favorite titles, and enjoy an immersive gaming experience like never before.</p>
                <h2>Real-Time Ray Tracing</h2>
                <p>Experience lifelike graphics and stunning visual effects with real-time ray tracing technology. The RTX 4070 Ti SUPER VENTUS 2X OC features dedicated ray tracing cores for ultra-realistic lighting, reflections, and shadows, bringing your games to life with cinematic detail.</p>
                <h2>AI-Powered DLSS</h2>
                <p>Take advantage of NVIDIAs AI-powered Deep Learning Super Sampling (DLSS) technology to enhance image quality and boost performance in supported games. Enjoy higher frame rates and smoother gameplay without compromising on image quality, giving you the competitive edge in fast-paced multiplayer titles.</p>
                <h2>Immersive 4K Gaming</h2>
                <p>With 16GB of ultra-fast GDDR6X memory and support for high-resolution displays, the RTX 4070 Ti SUPER VENTUS 2X OC is perfect for immersive 4K gaming experiences. Enjoy stunning visuals, rich textures, and smooth gameplay at the highest resolutions, and see every detail come to life on your screen.</p>
                <h2>Enhanced Connectivity</h2>
                <p>The RTX 4070 Ti SUPER VENTUS 2X OC features a range of connectivity options, including DisplayPort 1.4a and HDMI 2.1 ports, allowing you to connect to the latest high-resolution displays and VR headsets. Enjoy tear-free gaming and smooth, responsive gameplay at high refresh rates.</p>
                <h2>Dynamic RGB Lighting</h2>
                <p>Customize your gaming rig with MSIs Mystic Light RGB lighting technology. Choose from a variety of lighting effects and colors to match your setup, and synchronize your RGB lighting with other compatible components for a cohesive look. Make your PC stand out from the crowd with vibrant, customizable RGB lighting.</p>
                <h2>Powerful and Reliable</h2>
                <p>Backed by MSIs reputation for quality and reliability, the RTX 4070 Ti SUPER VENTUS 2X OC is built to last. With premium components and rigorous testing procedures, you can trust this graphics card to deliver exceptional performance and stability, whether youre gaming, streaming, or creating content.</p>
                <h2>Elevate Your Gaming Experience</h2>
                <p>With its powerful performance, advanced cooling technology, and immersive features, the MSI GeForce RTX 4070 Ti SUPER VENTUS 2X OC 16GB GDDR6X graphics card is the perfect choice for gamers who demand the best. Experience the next generation of gaming with MSI.</p>""",
                "sale_id": None,
            },
            {
                "id": 64,
                "name": "Gainward GeForce RTX 4080 Super Panther OC 16GB GDDR6X",
                "price": 1025.0,
                "old_price": 1035.0,
                "description": """<h2>Elevate Your Gaming Experience</h2>
                <p>Experience unparalleled gaming performance with the Gainward GeForce RTX 4080 Super Panther OC graphics card. Designed for enthusiasts and gamers who demand the ultimate in graphics performance, this GPU is equipped with 16GB of GDDR6X memory and advanced features to deliver smooth, immersive gaming experiences.</p>
                <h2>Powerful Performance</h2>
                <p>The RTX 4080 Super Panther OC features NVIDIAs Ampere architecture, delivering massive performance gains over previous generations. With a boost clock speed of XX MHz and XX CUDA cores, this graphics card is capable of handling the most demanding games and applications with ease.</p>
                <h2>Advanced Cooling Design</h2>
                <p>Stay cool under pressure with Gainwards custom cooling solution. The Super Panther OC features a triple-fan cooler with large heatsinks and heat pipes to keep temperatures in check during intense gaming sessions. With optimized fan curves and intelligent thermal management, you can push your GPU to the limit without worrying about overheating.</p>
                <h2>Factory Overclocked for Maximum Performance</h2>
                <p>Unlock extra performance right out of the box with Gainwards factory overclocked settings. The Super Panther OC features a boost clock speed of XX MHz, providing a significant performance boost compared to reference models. Experience higher frame rates, smoother gameplay, and faster rendering times in your favorite games and applications.</p>
                <h2>Real-Time Ray Tracing and DLSS</h2>
                <p>Experience lifelike graphics and stunning visual effects with real-time ray tracing technology. The RTX 4080 Super Panther OC features dedicated ray tracing cores for ultra-realistic lighting, reflections, and shadows, bringing your games to life with cinematic detail. With AI-powered Deep Learning Super Sampling (DLSS), you can enjoy higher frame rates and smoother gameplay without sacrificing image quality.</p>
                <h2>Immersive 4K Gaming</h2>
                <p>With 16GB of ultra-fast GDDR6X memory and support for high-resolution displays, the RTX 4080 Super Panther OC is perfect for immersive 4K gaming experiences. Enjoy stunning visuals, rich textures, and smooth gameplay at the highest resolutions, and see every detail come to life on your screen.</p>
                <h2>Customizable RGB Lighting</h2>
                <p>Personalize your gaming rig with Gainwards customizable RGB lighting. The Super Panther OC features RGB lighting on the fans and backplate, allowing you to customize the look of your graphics card to match your setup. Choose from a variety of lighting effects and colors to create your own unique gaming aesthetic.</p>
                <h2>Advanced Connectivity</h2>
                <p>The RTX 4080 Super Panther OC offers a range of connectivity options, including HDMI 2.1 and DisplayPort 1.4a, allowing you to connect to the latest high-resolution displays and VR headsets. With support for NVIDIA G-SYNC technology, you can enjoy tear-free gaming and smooth, responsive gameplay at high refresh rates.</p>
                <h2>Robust Build Quality</h2>
                <p>Backed by Gainwards reputation for quality and reliability, the RTX 4080 Super Panther OC is built to last. With premium components and rigorous testing procedures, you can trust this graphics card to deliver exceptional performance and stability, whether youre gaming, streaming, or creating content.</p>
                <h2>Take Your Gaming to the Next Level</h2>
                <p>With its powerful performance, advanced cooling design, and customizable RGB lighting, the Gainward GeForce RTX 4080 Super Panther OC 16GB GDDR6X graphics card is the ultimate choice for gamers and enthusiasts alike. Elevate your gaming experience and immerse yourself in the world of high-performance PC gaming with Gainward.</p>""",
                "sale_id": None,
            },
            {
                "id": 65,
                "name": "Sapphire Radeon RX 7800 XT PURE 16GB GDDR6",
                "price": 585.0,
                "old_price": 535.0,
                "description": """<h2>Elevate Your Gaming Experience</h2>
                <p>Experience next-level gaming performance with the Sapphire Radeon RX 7800 XT PURE graphics card. Designed for gamers who demand the best, this GPU is equipped with 16GB of GDDR6 memory and advanced features to deliver smooth, immersive gaming experiences.</p>
                <h2>Powerful Performance</h2>
                <p>The RX 7800 XT PURE features AMDs RDNA 3 architecture, delivering groundbreaking performance and stunning visual fidelity. With a boost clock speed of XX MHz and XX compute units, this graphics card is capable of handling the latest games and applications with ease.</p>
                <h2>Advanced Cooling Design</h2>
                <p>Stay cool under pressure with Sapphires custom cooling solution. The RX 7800 XT PURE features a triple-fan cooler with large heatsinks and heat pipes to keep temperatures in check during intense gaming sessions. With optimized fan curves and intelligent thermal management, you can push your GPU to the limit without worrying about overheating.</p>
                <h2>Factory Overclocked for Maximum Performance</h2>
                <p>Unlock extra performance right out of the box with Sapphires factory overclocked settings. The RX 7800 XT PURE features a boost clock speed of XX MHz, providing a significant performance boost compared to reference models. Experience higher frame rates, smoother gameplay, and faster rendering times in your favorite games and applications.</p>
                <h2>Real-Time Ray Tracing and FidelityFX Super Resolution</h2>
                <p>Experience lifelike graphics and stunning visual effects with real-time ray tracing technology. The RX 7800 XT PURE features dedicated ray tracing cores for ultra-realistic lighting, reflections, and shadows, bringing your games to life with cinematic detail. With AMDs FidelityFX Super Resolution (FSR), you can enjoy higher frame rates and smoother gameplay without sacrificing image quality.</p>
                <h2>Immersive 4K Gaming</h2>
                <p>With 16GB of ultra-fast GDDR6 memory and support for high-resolution displays, the RX 7800 XT PURE is perfect for immersive 4K gaming experiences. Enjoy stunning visuals, rich textures, and smooth gameplay at the highest resolutions, and see every detail come to life on your screen.</p>
                <h2>Customizable RGB Lighting</h2>
                <p>Personalize your gaming rig with Sapphires customizable RGB lighting. The RX 7800 XT PURE features RGB lighting on the fans and backplate, allowing you to customize the look of your graphics card to match your setup. Choose from a variety of lighting effects and colors to create your own unique gaming aesthetic.</p>
                <h2>Advanced Connectivity</h2>
                <p>The RX 7800 XT PURE offers a range of connectivity options, including HDMI 2.1 and DisplayPort 1.4, allowing you to connect to the latest high-resolution displays and VR headsets. With support for AMD FreeSync technology, you can enjoy tear-free gaming and smooth, responsive gameplay at high refresh rates.</p>
                <h2>Robust Build Quality</h2>
                <p>Backed by Sapphires reputation for quality and reliability, the RX 7800 XT PURE is built to last. With premium components and rigorous testing procedures, you can trust this graphics card to deliver exceptional performance and stability, whether youre gaming, streaming, or creating content.</p>
                <h2>Take Your Gaming to the Next Level</h2>
                <p>With its powerful performance, advanced cooling design, and customizable RGB lighting, the Sapphire Radeon RX 7800 XT PURE 16GB GDDR6 graphics card is the ultimate choice for gamers and enthusiasts alike. Elevate your gaming experience and immerse yourself in the world of high-performance PC gaming with Sapphire.</p>""",
                "sale_id": None,
            },
            {
                "id": 66,
                "name": "ASUS GeForce RTX 4090 ROG Strix Gaming White 24GB GDDR6X",
                "price": 2000.0,
                "old_price": 1950.0,
                "description": """<h2>Elevate Your Gaming Experience</h2>
                <p>Experience unparalleled gaming performance with the ASUS GeForce RTX 4090 ROG Strix Gaming White graphics card. Featuring a stunning white design, advanced cooling technology, and 24GB of GDDR6X memory, this GPU is engineered to deliver uncompromising performance for the most demanding gamers and enthusiasts.</p>
                <h2>Next-Generation Graphics Performance</h2>
                <p>Powered by NVIDIAs Ampere architecture, the RTX 4090 ROG Strix Gaming White delivers groundbreaking performance and unrivaled visual fidelity. With 24GB of ultra-fast GDDR6X memory and a boost clock speed of XX MHz, this graphics card is designed to handle the most demanding games and applications with ease.</p>
                <h2>Advanced Cooling Technology</h2>
                <p>Stay cool under pressure with ASUSs advanced cooling solution. The RTX 4090 ROG Strix Gaming White features a triple-fan cooler with Axial-tech fans and MaxContact technology to maximize airflow and heat dissipation. With a reinforced frame and precision-engineered heatsinks, this graphics card ensures optimal thermal performance even under heavy load.</p>
                <h2>Factory Overclocked for Maximum Performance</h2>
                <p>Unlock extra performance right out of the box with ASUSs factory overclocked settings. The RTX 4090 ROG Strix Gaming White features a boost clock speed of XX MHz, providing a significant performance boost compared to reference models. Experience higher frame rates, smoother gameplay, and faster rendering times in your favorite games and applications.</p>
                <h2>Real-Time Ray Tracing and DLSS</h2>
                <p>Experience lifelike graphics and stunning visual effects with real-time ray tracing technology. The RTX 4090 ROG Strix Gaming White features dedicated ray tracing cores for ultra-realistic lighting, reflections, and shadows, bringing your games to life with cinematic detail. With NVIDIA DLSS (Deep Learning Super Sampling), you can enjoy higher frame rates and smoother gameplay without sacrificing image quality.</p>
                <h2>Immersive 8K Gaming</h2>
                <p>With 24GB of ultra-fast GDDR6X memory and support for high-resolution displays, the RTX 4090 ROG Strix Gaming White is perfect for immersive 8K gaming experiences. Enjoy stunning visuals, rich textures, and smooth gameplay at the highest resolutions, and see every detail come to life on your screen.</p>
                <h2>Customizable RGB Lighting</h2>
                <p>Personalize your gaming rig with ASUSs customizable RGB lighting. The RTX 4090 ROG Strix Gaming White features RGB lighting on the fans and backplate, allowing you to customize the look of your graphics card to match your setup. Choose from a variety of lighting effects and colors to create your own unique gaming aesthetic.</p>
                <h2>Advanced Connectivity</h2>
                <p>The RTX 4090 ROG Strix Gaming White offers a range of connectivity options, including HDMI 2.1 and DisplayPort 1.4, allowing you to connect to the latest high-resolution displays and VR headsets. With support for NVIDIA G-SYNC technology, you can enjoy tear-free gaming and smooth, responsive gameplay at high refresh rates.</p>
                <h2>Robust Build Quality</h2>
                <p>Backed by ASUSs reputation for quality and reliability, the RTX 4090 ROG Strix Gaming White is built to last. With premium components and rigorous testing procedures, you can trust this graphics card to deliver exceptional performance and stability, whether youre gaming, streaming, or creating content.</p>
                <h2>Take Your Gaming to the Next Level</h2>
                <p>With its powerful performance, advanced cooling technology, and customizable RGB lighting, the ASUS GeForce RTX 4090 ROG Strix Gaming White 24GB GDDR6X graphics card is the ultimate choice for gamers and enthusiasts alike. Elevate your gaming experience and immerse yourself in the world of high-performance PC gaming with ASUS.</p>""",
                "sale_id": None,
            },
            {
                "id": 67,
                "name": "Lexar 32GB (2x16GB) 7200MHz CL34 ARES RGB Gaming",
                "price": 150.0,
                "old_price": 200.0,
                "description": """<h3>Lexar 32GB (2x16GB) 7200MHz CL34 ARES RGB Gaming Memory Kit</h3>
                <p>Elevate your gaming experience with the Lexar ARES RGB Gaming Memory Kit. Designed for high-performance gaming rigs, this memory kit combines blazing-fast speeds, ample capacity, and customizable RGB lighting to take your gaming to the next level.</p>
                <h3>Blazing-Fast Speeds</h3>
                <p>With a clock speed of 7200MHz and ultra-low CL34 latency, the Lexar ARES RGB Gaming Memory Kit delivers lightning-fast performance. Experience smoother gameplay, faster load times, and seamless multitasking with this high-speed memory kit.</p>
                <h3>Ample Capacity</h3>
                <p>Featuring a total capacity of 32GB (2x16GB), this memory kit provides ample space for storing your favorite games, applications, and multimedia files. Enjoy smooth performance and responsive multitasking, even with the most demanding tasks.</p>
                <h3>Customizable RGB Lighting</h3>
                <p>Enhance your gaming setup with customizable RGB lighting. The Lexar ARES RGB Gaming Memory Kit features dynamic RGB lighting effects that can be customized to match your gaming rigs aesthetic. Choose from a wide range of colors and lighting patterns to create your own unique look.</p>
                <h3>Optimized for Gaming</h3>
                <p>The Lexar ARES RGB Gaming Memory Kit is optimized for gaming performance. With its high-speed DDR4 memory and low-latency design, this memory kit ensures smooth gameplay, faster frame rates, and improved system responsiveness, giving you the competitive edge you need to dominate the battlefield.</p>
                <h3>Easy Installation</h3>
                <p>Installation is quick and easy with the Lexar ARES RGB Gaming Memory Kit. Simply plug the memory modules into your motherboards DIMM slots and secure them in place. The memory kit is compatible with most modern motherboards, ensuring hassle-free installation.</p>
                <h3>Reliable Performance</h3>
                <p>Backed by Lexars reputation for quality and reliability, the ARES RGB Gaming Memory Kit is built to last. Rigorously tested for compatibility and reliability, this memory kit is designed to withstand the rigors of gaming and deliver consistent performance over time.</p>
                <p>Transform your gaming experience with the Lexar ARES RGB Gaming Memory Kit. With its blazing-fast speeds, ample capacity, and customizable RGB lighting, this memory kit is the perfect choice for gamers who demand the best.</p>""",
                "sale_id": None,
            },
            {
                "id": 68,
                "name": "Kingston FURY 32GB (2x16GB) 5600MHz CL36 Beast Black EXPO AMD",
                "price": 50.0,
                "old_price": 70.0,
                "description": """<h3>Kingston FURY 32GB (2x16GB) 5600MHz CL36 Beast Black EXPO AMD Memory Kit</h3>
                <p>Upgrade your gaming rig with the Kingston FURY Beast Black EXPO AMD Memory Kit. Designed for high-performance gaming systems, this memory kit combines blazing-fast speeds, ample capacity, and reliable compatibility with AMD platforms to enhance your gaming experience.</p>
                <h3>Blazing-Fast Speeds</h3>
                <p>Featuring a lightning-fast clock speed of 5600MHz and ultra-low CL36 latency, the Kingston FURY Beast Black EXPO AMD Memory Kit delivers exceptional performance for gaming and multitasking. Experience smoother gameplay, faster load times, and improved system responsiveness with this high-speed memory kit.</p>
                <h3>Ample Capacity</h3>
                <p>With a total capacity of 32GB (2x16GB), this memory kit provides ample space for storing your favorite games, applications, and multimedia files. Enjoy smooth performance and seamless multitasking, even with the most demanding tasks.</p>
                <h3>Optimized for AMD Platforms</h3>
                <p>The Kingston FURY Beast Black EXPO AMD Memory Kit is specially optimized for compatibility with AMD platforms, ensuring reliable performance and seamless integration with your AMD-powered gaming system. Experience maximum stability and compatibility with AMD Ryzen processors and motherboards.</p>
                <h3>Stylish Design</h3>
                <p>Featuring a sleek black design, the Kingston FURY Beast Black EXPO AMD Memory Kit adds a touch of style to your gaming rig. The low-profile heat spreader not only looks great but also helps dissipate heat for improved thermal performance.</p>
                <h3>Easy Installation</h3>
                <p>Installation is quick and easy with the Kingston FURY Beast Black EXPO AMD Memory Kit. Simply plug the memory modules into your motherboards DIMM slots and secure them in place. The memory kit is compatible with most modern motherboards, ensuring hassle-free installation.</p>
                <h3>Reliable Performance</h3>
                <p>Backed by Kingstons reputation for quality and reliability, the FURY Beast Black EXPO AMD Memory Kit is built to last. Rigorously tested for compatibility and reliability, this memory kit is designed to withstand the rigors of gaming and deliver consistent performance over time.</p>
                <p>Take your gaming to the next level with the Kingston FURY Beast Black EXPO AMD Memory Kit. With its blazing-fast speeds, ample capacity, and stylish design, this memory kit is the perfect choice for gamers who demand the best.</p>""",
                "sale_id": 6,
            },
            {
                "id": 69,
                "name": "GOODRAM 32GB (2x16GB) 3600MHz CL18 IRDM PRO Deep Black",
                "price": 100.0,
                "old_price": 135.0,
                "description": """<h3>GOODRAM 32GB (2x16GB) 3600MHz CL18 IRDM PRO Deep Black Memory Kit</h3>
                <p>Elevate your systems performance with the GOODRAM IRDM PRO Deep Black Memory Kit. Designed for enthusiasts and gamers, this memory kit offers high-speed performance, ample capacity, and sleek aesthetics to enhance your computing experience.</p>
                <h3>High-Speed Performance</h3>
                <p>Featuring a clock speed of 3600MHz and low CL18 latency, the GOODRAM IRDM PRO Deep Black Memory Kit delivers blazing-fast performance for smooth multitasking, gaming, and content creation. Experience improved system responsiveness and faster data transfer speeds with this high-speed memory kit.</p>
                <h3>Ample Capacity</h3>
                <p>With a total capacity of 32GB (2x16GB), this memory kit provides ample space for running demanding applications, multitasking with multiple programs, and storing large files. Enjoy seamless performance and smooth multitasking without worrying about running out of memory.</p>
                <h3>Sleek Aesthetics</h3>
                <p>The GOODRAM IRDM PRO Deep Black Memory Kit features a stylish design with a deep black heat spreader that adds a touch of elegance to your system. The sleek aesthetics complement any build and enhance the overall look of your gaming rig or workstation.</p>
                <h3>Optimized Compatibility</h3>
                <p>Designed for compatibility with a wide range of motherboards, the GOODRAM IRDM PRO Deep Black Memory Kit ensures seamless integration and reliable performance. Whether youre building a new system or upgrading an existing one, this memory kit is compatible with most modern platforms.</p>
                <h3>Enhanced Cooling</h3>
                <p>The heat spreader on the GOODRAM IRDM PRO Deep Black Memory Kit is designed to efficiently dissipate heat and keep the memory modules cool during intense gaming sessions or heavy workloads. Enjoy enhanced thermal performance and improved stability, even under demanding conditions.</p>
                <h3>Easy Installation</h3>
                <p>Installation is quick and easy with the GOODRAM IRDM PRO Deep Black Memory Kit. Simply insert the memory modules into the appropriate DIMM slots on your motherboard and secure them in place. The memory kit is compatible with most standard DDR4 slots, ensuring hassle-free installation.</p>
                <h3>Reliable Performance</h3>
                <p>Backed by GOODRAMs reputation for quality and reliability, the IRDM PRO Deep Black Memory Kit is built to last. Each memory module undergoes rigorous testing to ensure optimal performance, compatibility, and stability, so you can trust your system to perform flawlessly.</p>
                <p>Upgrade your system with the GOODRAM IRDM PRO Deep Black Memory Kit and experience the ultimate combination of speed, capacity, and style. Whether youre gaming, creating content, or multitasking, this memory kit delivers the performance and reliability you need.</p>""",
                "sale_id": None,
            },
            {
                "id": 70,
                "name": "Patriot 32GB (2x16GB) 6000MHz CL36 VIPER VENOM",
                "price": 120.0,
                "old_price": 135.0,
                "description": """<h3>Patriot 32GB (2x16GB) 6000MHz CL36 VIPER VENOM Memory Kit</h3>
                <p>Upgrade your gaming experience with the Patriot VIPER VENOM Memory Kit. Designed for high-performance systems, this memory kit offers blazing-fast speeds, ample capacity, and reliable performance to take your gaming to the next level.</p>
                <h3>Blazing-Fast Speeds</h3>
                <p>The Patriot VIPER VENOM Memory Kit boasts a clock speed of 6000MHz, delivering lightning-fast performance for seamless gaming and multitasking. With ultra-low CL36 latency, you can enjoy responsive gameplay and smooth system operation even during intense gaming sessions.</p>
                <h3>Ample Capacity</h3>
                <p>With a total capacity of 32GB (2x16GB), this memory kit provides ample space for running demanding games, multitasking with multiple applications, and handling large files. Experience enhanced performance and improved productivity without worrying about running out of memory.</p>
                <h3>Extreme Performance</h3>
                <p>Designed for extreme overclocking, the Patriot VIPER VENOM Memory Kit is optimized for maximum performance and stability. Whether youre pushing your system to the limit or competing in eSports tournaments, this memory kit delivers the speed and reliability you need to stay ahead of the competition.</p>
                <h3>Enhanced Cooling</h3>
                <p>The VIPER VENOM Memory Kit features a high-quality heat spreader designed to dissipate heat and keep the memory modules cool under heavy load. Enjoy improved thermal performance and increased reliability, even during extended gaming sessions or overclocking.</p>
                <h3>Customizable RGB Lighting</h3>
                <p>Add style to your gaming rig with customizable RGB lighting effects. The VIPER VENOM Memory Kit features RGB lighting that can be customized to match your gaming setup or mood. Choose from a wide range of colors and effects to create the perfect ambiance for your gaming environment.</p>
                <h3>Easy Installation</h3>
                <p>Installation is quick and easy with the Patriot VIPER VENOM Memory Kit. Simply insert the memory modules into the appropriate DIMM slots on your motherboard and secure them in place. The memory kit is compatible with most standard DDR4 slots, ensuring hassle-free installation.</p>
                <h3>Reliable Performance</h3>
                <p>Backed by Patriots reputation for quality and reliability, the VIPER VENOM Memory Kit is built to last. Each memory module undergoes rigorous testing to ensure optimal performance, compatibility, and stability, so you can trust your system to perform flawlessly.</p>
                <p>Elevate your gaming experience with the Patriot VIPER VENOM Memory Kit and unleash the full potential of your system. With ultra-fast speeds, ample capacity, and customizable RGB lighting, this memory kit delivers the performance and style you need to dominate the competition.</p>""",
                "sale_id": None,
            },
            {
                "id": 71,
                "name": "Lexar 32GB (2x16GB) 3200MHz CL16 Thor",
                "price": 80.0,
                "old_price": 95.0,
                "description": """<h2>Lexar 32GB (2x16GB) 3200MHz CL16 Thor Memory Kit</h2>
                <p>Upgrade your systems memory with the Lexar Thor Memory Kit, offering impressive performance and reliability for your computing needs.</p>
                <h2>High-Speed Performance</h2>
                <p>The Lexar Thor Memory Kit boasts a clock speed of 3200MHz, providing fast and responsive performance for multitasking, gaming, and multimedia applications. With low CL16 latency, you can experience smooth and efficient operation even during demanding tasks.</p>
                <h2>Ample Capacity</h2>
                <p>With a total capacity of 32GB (2x16GB), this memory kit offers ample space for running multiple applications simultaneously, handling large files, and storing multimedia content. Enjoy improved performance and responsiveness without worrying about running out of memory.</p>
                <h2>Reliable Stability</h2>
                <p>Designed for stability and reliability, the Lexar Thor Memory Kit ensures consistent performance under various workloads. Whether youre gaming, editing videos, or running productivity software, you can rely on this memory kit to deliver reliable operation.</p>
                <h2>Enhanced Cooling</h2>
                <p>The Lexar Thor Memory Kit features a heat spreader design to dissipate heat effectively, keeping the memory modules cool during extended use. This helps maintain optimal performance and stability, even under heavy workloads or overclocking sPRICErios.</p>
                <h2>Plug-and-Play Installation</h2>
                <p>Installation is quick and hassle-free with the Lexar Thor Memory Kit. Simply insert the memory modules into the appropriate DIMM slots on your motherboard, and the memory will be automatically detected. Enjoy seamless integration and instant performance improvements.</p>
                <h2>Compatibility</h2>
                <p>The Lexar Thor Memory Kit is compatible with a wide range of desktop systems, making it easy to upgrade your existing setup. Whether youre building a new PC or upgrading an older system, this memory kit offers compatibility with most modern motherboards.</p>
                <h2>Ideal for Gaming and Productivity</h2>
                <p>Whether youre a gamer, content creator, or power user, the Lexar Thor Memory Kit delivers the performance and reliability you need. Boost your gaming experience, enhance your productivity, and enjoy smooth multitasking with this high-quality memory solution.</p>
                <h2>Conclusion</h2>
                <p>Upgrade your system with the Lexar Thor Memory Kit and experience improved performance, reliability, and responsiveness. With fast speeds, ample capacity, and enhanced cooling, this memory kit is an ideal choice for gamers, professionals, and enthusiasts alike.</p>""",
                "sale_id": None,
            },
            {
                "id": 72,
                "name": "Kingston FURY 32GB (2x16GB) 3600MHz CL16 Renegade Black",
                "price": 90.0,
                "old_price": 95.0,
                "description": """<h2>Kingston FURY 32GB (2x16GB) 3600MHz CL16 Renegade Black Memory Kit</h2>
                <p>Elevate your gaming experience and system performance with the Kingston FURY Renegade Black Memory Kit. Engineered for speed, reliability, and style, this memory kit enhances your gaming rigs capabilities and ensures smooth multitasking for demanding tasks.</p>
                <h2>High-Speed Performance</h2>
                <p>The Kingston FURY Renegade Black Memory Kit operates at a blistering speed of 3600MHz, providing lightning-fast responsiveness and seamless multitasking capabilities. With low CL16 latency, it delivers quick data access and ensures smooth performance even during intense gaming sessions or content creation tasks.</p>
                <h2>Enhanced Gaming Experience</h2>
                <p>Designed specifically for gamers, the Kingston FURY Renegade Black Memory Kit offers the perfect combination of speed and capacity to handle modern AAA titles and high-resolution gaming. Enjoy faster load times, smoother gameplay, and reduced stuttering for an immersive gaming experience.</p>
                <h2>Reliable Stability</h2>
                <p>Backed by Kingstons renowned reliability and quality assurance, the FURY Renegade Black Memory Kit delivers consistent performance and stability under various workloads. Whether youre overclocking your system or running resource-intensive applications, you can count on this memory kit to maintain reliable operation.</p>
                <h2>Aggressive Design</h2>
                <p>The Kingston FURY Renegade Black Memory Kit features a sleek and aggressive design with black heat spreaders that complement any gaming setup. The premium aesthetics add a touch of style to your rig while ensuring efficient heat dissipation for optimal performance.</p>
                <h2>Plug-and-Play Installation</h2>
                <p>Installation is hassle-free with the Kingston FURY Renegade Black Memory Kit. Simply insert the memory modules into the appropriate DIMM slots on your motherboard, and they will be automatically detected. Enjoy seamless integration and instant performance enhancements without any manual configuration.</p>
                <h2>Compatibility</h2>
                <p>Compatible with most modern Intel and AMD platforms, the Kingston FURY Renegade Black Memory Kit offers broad compatibility for hassle-free installation in a wide range of gaming systems. Whether youre building a new PC or upgrading an existing one, this memory kit ensures compatibility and reliability.</p>
                <h2>Ideal for Enthusiasts and Gamers</h2>
                <p>Whether youre a hardcore gamer, overclocking enthusiast, or power user, the Kingston FURY Renegade Black Memory Kit delivers the speed, performance, and reliability you need to stay ahead of the competition. Elevate your gaming experience and unleash the full potential of your system with this high-performance memory solution.</p>
                <h2>Conclusion</h2>
                <p>Upgrade your gaming rig with the Kingston FURY Renegade Black Memory Kit and experience unparalleled speed, reliability, and style. With its high-speed performance, aggressive design, and plug-and-play installation, this memory kit is the perfect choice for gamers and enthusiasts seeking uncompromising performance and aesthetics.</p>""",
                "sale_id": None,
            },
            {
                "id": 73,
                "name": "Lexar 32GB (2x16GB) 3600MHz CL18 Thor",
                "price": 100.0,
                "old_price": 105.0,
                "description": """<h2>Lexar 32GB (2x16GB) 3600MHz CL18 Thor Memory Kit</h2>
                <p>Elevate your gaming and computing experience with the Lexar Thor Memory Kit. Engineered for high-speed performance and reliability, this memory kit ensures seamless multitasking, smooth gaming, and efficient data handling for demanding tasks.</p>
                <h2>Blazing Fast Performance</h2>
                <p>The Lexar Thor Memory Kit operates at a lightning-fast speed of 3600MHz, delivering rapid data access and responsiveness for enhanced system performance. With low CL18 latency, it ensures quick access to stored data, resulting in smoother multitasking and reduced loading times for applications and games.</p>
                <h2>Optimized for Gaming</h2>
                <p>Designed for gaming enthusiasts and power users, the Lexar Thor Memory Kit offers the perfect balance of speed and capacity to handle intensive gaming sessions and resource-heavy tasks with ease. Enjoy faster frame rates, snappier gameplay, and improved system responsiveness for an immersive gaming experience.</p>
                <h2>Reliable Stability</h2>
                <p>Backed by Lexars reputation for quality and reliability, the Thor Memory Kit delivers consistent performance and stability under various workloads. Whether youre gaming, streaming, or running demanding applications, you can rely on this memory kit to maintain optimal performance without compromise.</p>
                <h2>Efficient Heat Dissipation</h2>
                <p>The Lexar Thor Memory Kit features a heat spreader design that efficiently dissipates heat to ensure reliable performance even during prolonged gaming sessions or heavy workloads. The heat spreaders help prevent overheating and ensure stable operation, allowing you to push your system to its limits without worrying about thermal throttling.</p>
                <h2>Plug-and-Play Installation</h2>
                <p>Installation is quick and easy with the Lexar Thor Memory Kit. Simply insert the memory modules into the appropriate DIMM slots on your motherboard, and they will be automatically recognized by the system. Enjoy hassle-free setup and instant performance enhancements without the need for manual configuration.</p>
                <h2>Compatibility</h2>
                <p>The Lexar Thor Memory Kit is compatible with a wide range of Intel and AMD platforms, ensuring broad compatibility and seamless integration with your gaming or productivity setup. Whether youre building a new system or upgrading an existing one, this memory kit provides the compatibility and performance you need.</p>
                <h2>Enhanced Productivity</h2>
                <p>Boost your productivity and efficiency with the Lexar Thor Memory Kit. Whether youre multitasking, video editing, or running virtual machines, this memory kit ensures smooth performance and responsiveness for demanding tasks. Experience faster data access and smoother workflow transitions with this high-performance memory solution.</p>
                <h2>Conclusion</h2>
                <p>Upgrade your gaming rig or productivity workstation with the Lexar Thor Memory Kit and experience enhanced speed, reliability, and performance. With its blazing-fast speed, optimized gaming performance, and reliable stability, this memory kit is the perfect choice for gamers, content creators, and power users seeking uncompromising performance and reliability.</p>""",
                "sale_id": None,
            },
            {
                "id": 74,
                "name": "Patriot 64GB (2x32GB) 6000MHz CL36 Viper VENOM",
                "price": 200.0,
                "old_price": 250.0,
                "description": """<h2>Patriot 64GB (2x32GB) 6000MHz CL36 Viper VENOM Memory Kit</h2>
                <p>Elevate your gaming and computing experience with the Patriot Viper VENOM Memory Kit. Engineered for high-speed performance and reliability, this memory kit ensures seamless multitasking, smooth gaming, and efficient data handling for demanding tasks.</p>
                <h2>Blazing Fast Performance</h2>
                <p>The Patriot Viper VENOM Memory Kit operates at an impressive speed of 6000MHz, delivering lightning-fast data access and responsiveness for enhanced system performance. With low CL36 latency, it ensures quick access to stored data, resulting in smoother multitasking and reduced loading times for applications and games.</p>
                <h2>Optimized for Gaming</h2>
                <p>Designed for gaming enthusiasts and power users, the Patriot Viper VENOM Memory Kit offers the perfect balance of speed and capacity to handle intensive gaming sessions and resource-heavy tasks with ease. Enjoy faster frame rates, snappier gameplay, and improved system responsiveness for an immersive gaming experience.</p>
                <h2>Reliable Stability</h2>
                <p>Backed by Patriots reputation for quality and reliability, the Viper VENOM Memory Kit delivers consistent performance and stability under various workloads. Whether youre gaming, streaming, or running demanding applications, you can rely on this memory kit to maintain optimal performance without compromise.</p>
                <h2>Efficient Heat Dissipation</h2>
                <p>The Patriot Viper VENOM Memory Kit features a heat spreader design that efficiently dissipates heat to ensure reliable performance even during prolonged gaming sessions or heavy workloads. The heat spreaders help prevent overheating and ensure stable operation, allowing you to push your system to its limits without worrying about thermal throttling.</p>
                <h2>Plug-and-Play Installation</h2>
                <p>Installation is quick and easy with the Patriot Viper VENOM Memory Kit. Simply insert the memory modules into the appropriate DIMM slots on your motherboard, and they will be automatically recognized by the system. Enjoy hassle-free setup and instant performance enhancements without the need for manual configuration.</p>
                <h2>Compatibility</h2>
                <p>The Patriot Viper VENOM Memory Kit is compatible with a wide range of Intel and AMD platforms, ensuring broad compatibility and seamless integration with your gaming or productivity setup. Whether youre building a new system or upgrading an existing one, this memory kit provides the compatibility and performance you need.</p>
                <h2>Enhanced Productivity</h2>
                <p>Boost your productivity and efficiency with the Patriot Viper VENOM Memory Kit. Whether youre multitasking, video editing, or running virtual machines, this memory kit ensures smooth performance and responsiveness for demanding tasks. Experience faster data access and smoother workflow transitions with this high-performance memory solution.</p>
                <h2>Conclusion</h2>
                <p>Upgrade your gaming rig or productivity workstation with the Patriot Viper VENOM Memory Kit and experience enhanced speed, reliability, and performance. With its blazing-fast speed, optimized gaming performance, and reliable stability, this memory kit is the perfect choice for gamers, content creators, and power users seeking uncompromising performance and reliability.</p>""",
                "sale_id": None,
            },
            {
                "id": 75,
                "name": "Kingston FURY 16GB (2x16GB) 3600MHz CL16 Renegade Black",
                "price": 100.0,
                "old_price": 135.0,
                "description": """<h2>Kingston FURY 16GB (2x16GB) 3600MHz CL16 Renegade Black Memory Kit</h2>
                <p>Elevate your gaming experience and system performance with the Kingston FURY Renegade Black Memory Kit. Designed for enthusiasts and gamers, this memory kit delivers high-speed performance, reliability, and impressive aesthetics to enhance your gaming rig.</p>
                <h2>Blazing Speed</h2>
                <p>The Kingston FURY Renegade Black Memory Kit operates at an impressive speed of 3600MHz, providing lightning-fast data access and seamless multitasking. With low CL16 latency, it ensures quick response times and reduced loading times for applications and games, giving you a competitive edge in gaming and productivity tasks.</p>
                <h2>Optimized for Gaming</h2>
                <p>Engineered for gaming enthusiasts, the Kingston FURY Renegade Black Memory Kit offers the perfect combination of speed and capacity to handle demanding gaming sessions and intensive workloads. Experience smoother gameplay, faster frame rates, and improved system responsiveness for an immersive gaming experience.</p>
                <h2>Enhanced Aesthetics</h2>
                <p>Featuring a sleek black heatsink with a stylish design, the Kingston FURY Renegade Black Memory Kit adds a touch of elegance to your gaming rig. The black heatsink not only looks great but also helps dissipate heat effectively to ensure reliable performance during extended gaming sessions or heavy workloads.</p>
                <h2>Reliable Performance</h2>
                <p>Backed by Kingstons reputation for quality and reliability, the FURY Renegade Black Memory Kit delivers consistent performance and stability under various conditions. Whether youre gaming, streaming, or multitasking, you can count on this memory kit to maintain optimal performance without compromise.</p>
                <h2>Plug-and-Play Installation</h2>
                <p>Installation is quick and easy with the Kingston FURY Renegade Black Memory Kit. Simply insert the memory modules into the appropriate DIMM slots on your motherboard, and they will be automatically recognized by the system. Enjoy hassle-free setup and instant performance enhancements without the need for manual configuration.</p>
                <h2>Compatibility</h2>
                <p>The Kingston FURY Renegade Black Memory Kit is compatible with a wide range of Intel and AMD platforms, ensuring broad compatibility and seamless integration with your gaming setup. Whether youre building a new gaming rig or upgrading an existing one, this memory kit provides the compatibility and performance you need.</p>
                <h2>Conclusion</h2>
                <p>Upgrade your gaming rig with the Kingston FURY Renegade Black Memory Kit and experience enhanced speed, reliability, and aesthetics. With its blazing-fast speed, optimized gaming performance, and stylish design, this memory kit is the perfect choice for gamers seeking uncompromising performance and style.</p>""",
                "sale_id": None,
            },
            {
                "id": 76,
                "name": "Patriot 32GB (2x16GB) 3600MHz CL18 Viper Steel",
                "price": 56.0,
                "old_price": 78.0,
                "description": """<h2>Patriot 32GB (2x16GB) 3600MHz CL18 Viper Steel Memory Kit</h2>
                <p>Upgrade your systems performance with the Patriot Viper Steel Memory Kit. Designed for enthusiasts and gamers, this memory kit delivers high-speed performance, reliability, and exceptional multitasking capabilities to enhance your computing experience.</p>
                <h2>Blazing Speed</h2>
                <p>The Patriot Viper Steel Memory Kit operates at a blistering speed of 3600MHz, providing lightning-fast data access and seamless multitasking. With low CL18 latency, it ensures quick response times and reduced loading times for applications and games, boosting overall system performance.</p>
                <h2>Enhanced Gaming Performance</h2>
                <p>Engineered for gaming enthusiasts, the Patriot Viper Steel Memory Kit offers the perfect combination of speed and capacity to handle demanding gaming sessions and intensive workloads. Experience smoother gameplay, faster frame rates, and improved system responsiveness for an immersive gaming experience.</p>
                <h2>Robust Construction</h2>
                <p>Featuring a sleek and durable aluminum heat spreader, the Patriot Viper Steel Memory Kit not only looks great but also helps dissipate heat effectively to ensure reliable performance during extended gaming sessions or heavy workloads. The heat spreaders low-profile design ensures compatibility with most CPU coolers.</p>
                <h2>Plug-and-Play Installation</h2>
                <p>Installation is quick and easy with the Patriot Viper Steel Memory Kit. Simply insert the memory modules into the appropriate DIMM slots on your motherboard, and they will be automatically recognized by the system. Enjoy hassle-free setup and instant performance enhancements without the need for manual configuration.</p>
                <h2>Reliable Performance</h2>
                <p>Backed by Patriots reputation for quality and reliability, the Viper Steel Memory Kit delivers consistent performance and stability under various conditions. Whether youre gaming, streaming, or multitasking, you can count on this memory kit to maintain optimal performance without compromise.</p>
                <h2>Compatibility</h2>
                <p>The Patriot Viper Steel Memory Kit is compatible with a wide range of Intel and AMD platforms, ensuring broad compatibility and seamless integration with your system. Whether youre building a new gaming rig or upgrading an existing one, this memory kit provides the compatibility and performance you need.</p>
                <h2>Conclusion</h2>
                <p>Upgrade your system with the Patriot Viper Steel Memory Kit and experience enhanced speed, reliability, and multitasking capabilities. With its blazing-fast speed, robust construction, and plug-and-play installation, this memory kit is the perfect choice for gamers and enthusiasts seeking uncompromising performance and reliability.</p>""",
                "sale_id": None,
            },
            {
                "id": 77,
                "name": "Gigabyte B650M GAMING X AX",
                "price": 256.0,
                "old_price": 278.0,
                "description": """<h3>Gigabyte B650M GAMING X AX: Elevate Your Gaming Experience</h3>
                <p>Experience the ultimate gaming performance and immersive visuals with the Gigabyte B650M GAMING X AX motherboard. Designed for gamers and enthusiasts, this motherboard combines cutting-edge features, robust construction, and advanced technologies to deliver an unparalleled gaming experience.</p>
                <h3>Powerful Performance</h3>
                <p>Powered by the latest Intel B650 chipset, the Gigabyte B650M GAMING X AX motherboard supports 12th generation Intel Core processors, providing exceptional performance for gaming, content creation, and multitasking. With support for DDR5 memory and PCIe 5.0 technology, this motherboard delivers lightning-fast data transfer speeds and responsive system performance.</p>
                <h3>Immersive Gaming Experience</h3>
                <p>Immerse yourself in the action with the Gigabyte B650M GAMING X AX motherboard. Equipped with advanced audio technologies and high-quality components, including AMP-UP Audio and Nichicon Fine Gold capacitors, this motherboard delivers immersive sound and crystal-clear audio for a lifelike gaming experience.</p>
                <h3>Enhanced Connectivity</h3>
                <p>Stay connected and experience lag-free gaming with the Gigabyte B650M GAMING X AX motherboard. Featuring high-speed Ethernet LAN, Wi-Fi 6E connectivity, and Bluetooth 5.2 support, this motherboard ensures seamless online gaming and networking performance.</p>
                <h3>Advanced Cooling Solutions</h3>
                <p>Keep your system cool and stable during intense gaming sessions with the Gigabyte B650M GAMING X AX motherboard. Equipped with advanced cooling solutions, including multi-zone heatsinks and Smart Fan technology, this motherboard ensures efficient heat dissipation and optimal thermal performance for your components.</p>
                <h3>RGB Fusion 3.0</h3>
                <p>Customize your gaming rig with vibrant RGB lighting effects using Gigabytes RGB Fusion 3.0 software. With support for addressable RGB headers and customizable LED effects, you can personalize your systems lighting to match your gaming setup and create stunning visual effects.</p>
                <h3>User-Friendly Design</h3>
                <p>The Gigabyte B650M GAMING X AX motherboard features a user-friendly design with intuitive BIOS settings and easy-to-use overclocking tools. With Gigabytes exclusive Q-Flash Plus technology, you can easily update your BIOS without installing a CPU or memory, ensuring hassle-free maintenance and optimization.</p>
                <p>Elevate your gaming experience to the next level with the Gigabyte B650M GAMING X AX motherboard. Whether youre a casual gamer or a competitive esports enthusiast, this motherboard provides the performance, features, and reliability you need for the ultimate gaming experience.</p>""",
                "sale_id": None,
            },
            {
                "id": 78,
                "name": "MSI MAG B650 TOMAHAWK WIFI",
                "price": 200.0,
                "old_price": 220.0,
                "description": """<h3>MSI MAG B650 TOMAHAWK WIFI: Unleash Your Gaming Potential</h3>
                <p>Experience the next level of gaming performance with the MSI MAG B650 TOMAHAWK WIFI motherboard. Designed to meet the demands of gamers and enthusiasts, this motherboard combines powerful features, robust construction, and advanced technologies to deliver an exceptional gaming experience.</p>
                <h3>Powerful Performance</h3>
                <p>Powered by the latest Intel B650 chipset, the MSI MAG B650 TOMAHAWK WIFI motherboard supports 12th generation Intel Core processors, offering unparalleled performance for gaming, content creation, and multitasking. With support for DDR5 memory and PCIe 5.0 technology, this motherboard delivers blazing-fast data transfer speeds and responsive system performance.</p>
                <h3>Enhanced Gaming Connectivity</h3>
                <p>Stay connected and experience lag-free gaming with the MSI MAG B650 TOMAHAWK WIFI motherboard. Featuring built-in Wi-Fi 6E connectivity and high-speed Ethernet LAN, this motherboard ensures seamless online gaming and networking performance. Plus, with Bluetooth 5.2 support, you can easily connect your favorite peripherals and accessories.</p>
                <h3>Immersive Gaming Audio</h3>
                <p>Immerse yourself in the action with the MSI MAG B650 TOMAHAWK WIFI motherboards high-quality audio solutions. Equipped with Audio Boost technology and Nahimic audio enhancer, this motherboard delivers immersive sound and crystal-clear audio for a truly immersive gaming experience.</p>
                <h3>Advanced Cooling Solutions</h3>
                <p>Keep your system cool and stable during intense gaming sessions with the MSI MAG B650 TOMAHAWK WIFI motherboard. Featuring an extended heatsink design and Frozr AI Cooling technology, this motherboard ensures efficient heat dissipation and optimal thermal performance for your components, even under heavy load.</p>
                <h3>Personalized RGB Lighting</h3>
                <p>Customize your gaming rig with vibrant RGB lighting effects using MSIs Mystic Light software. With support for customizable LED effects and multiple RGB headers, you can personalize your systems lighting to match your gaming setup and create stunning visual effects.</p>
                <h3>User-Friendly Design</h3>
                <p>The MSI MAG B650 TOMAHAWK WIFI motherboard features a user-friendly design with intuitive BIOS settings and easy-to-use overclocking tools. With MSIs exclusive Click BIOS 5 interface, you can easily fine-tune your system settings and maximize performance with just a few clicks.</p>
                <p>Unleash your gaming potential with the MSI MAG B650 TOMAHAWK WIFI motherboard. Whether youre a casual gamer or a hardcore enthusiast, this motherboard provides the performance, features, and reliability you need to dominate the competition and take your gaming experience to the next level.</p>""",
                "sale_id": None,
            },
            {
                "id": 79,
                "name": "ASUS PRIME B660-PLUS DDR4",
                "price": 150.0,
                "old_price": 178.0,
                "description": """<h3>ASUS PRIME B660-PLUS DDR4: Elevate Your PC Experience</h3>
                <p>Experience reliable performance and advanced features with the ASUS PRIME B660-PLUS DDR4 motherboard. Designed for productivity and everyday computing tasks, this motherboard combines ASUS renowned quality with the latest technologies to provide a seamless computing experience.</p>
                <h3>Powerful Performance</h3>
                <p>The ASUS PRIME B660-PLUS DDR4 motherboard is powered by the Intel B660 chipset, offering support for 12th generation Intel Core processors. With DDR4 memory support and PCIe 4.0 technology, this motherboard delivers fast and responsive performance for multitasking, content creation, and everyday computing tasks.</p>
                <h3>Comprehensive Connectivity</h3>
                <p>Stay connected and productive with the ASUS PRIME B660-PLUS DDR4 motherboards comprehensive connectivity options. Equipped with multiple USB ports, including USB 3.2 Gen 2 and USB-C, as well as Gigabit LAN and PCIe slots, this motherboard provides ample connectivity for all your devices and peripherals.</p>
                <h3>Enhanced Audio</h3>
                <p>Immerse yourself in high-quality audio with the ASUS PRIME B660-PLUS DDR4 motherboards built-in audio solutions. Featuring ASUS exclusive audio technologies, including Realtek S1200A codec and audio shielding, this motherboard delivers crystal-clear sound for an immersive multimedia experience.</p>
                <h3>Stable and Reliable</h3>
                <p>Designed with durability and reliability in mind, the ASUS PRIME B660-PLUS DDR4 motherboard features high-quality components and industry-leading ASUS reliability standards. With ASUS comprehensive cooling solutions and advanced power delivery, this motherboard ensures stable operation even under heavy load.</p>
                <h3>User-Friendly Design</h3>
                <p>The ASUS PRIME B660-PLUS DDR4 motherboard features a user-friendly design with ASUS intuitive UEFI BIOS interface. With EZ Mode for beginners and Advanced Mode for experienced users, you can easily customize settings, monitor system performance, and overclock your CPU with ease.</p>
                <h3>ASUS AI Networking</h3>
                <p>Optimize your network performance with ASUS AI Networking technology. This intelligent networking solution automatically prioritizes gaming packets for smoother online gaming and streaming, while reducing latency and lag for a seamless online experience.</p>
                <p>Elevate your PC experience with the ASUS PRIME B660-PLUS DDR4 motherboard. Whether youre building a new system or upgrading your existing one, this motherboard offers the performance, reliability, and features you need to take your computing to the next level.</p>""",
                "sale_id": None,
            },
            {
                "id": 80,
                "name": "MSI Z790 GAMING PLUS WIFI",
                "price": 250.0,
                "old_price": 258.0,
                "description": """<h3>MSI Z790 GAMING PLUS WIFI: Elevate Your Gaming Experience</h3>
                <p>Experience the ultimate gaming performance with the MSI Z790 GAMING PLUS WIFI motherboard. Engineered for gamers and enthusiasts, this motherboard combines cutting-edge technology with exceptional features to deliver an immersive gaming experience like no other.</p>
                <h3>Unleash the Power of 12th Gen Intel Core Processors</h3>
                <p>The MSI Z790 GAMING PLUS WIFI motherboard supports 12th generation Intel Core processors, allowing you to unlock the full potential of your gaming rig. With support for DDR5 memory and PCIe 5.0 technology, this motherboard provides blazing-fast performance for demanding gaming sessions and multitasking.</p>
                <h3>Immersive Gaming Audio</h3>
                <p>Dive into the action with immersive gaming audio powered by MSI Audio Boost technology. Featuring a high-quality audio processor and premium audio components, including Nahimic audio enhancer, this motherboard delivers crystal-clear sound with enhanced spatial awareness for a truly immersive gaming experience.</p>
                <h3>Advanced Cooling Solutions</h3>
                <p>Keep your system cool and stable during intense gaming sessions with MSIs advanced cooling solutions. Equipped with an extended heatsink design, M.2 Shield Frozr, and Frozr AI Cooling, this motherboard ensures optimal thermal performance for your components, allowing you to push your system to its limits without overheating.</p>
                <h3>Seamless Connectivity</h3>
                <p>Stay connected with lightning-fast connectivity options on the MSI Z790 GAMING PLUS WIFI motherboard. Featuring built-in WiFi 6E, 2.5G LAN, and USB 3.2 Gen 2x2 ports, this motherboard offers high-speed data transfer and low-latency networking for lag-free online gaming and smooth multimedia streaming.</p>
                <h3>Personalized Gaming Experience</h3>
                <p>Customize your gaming rig with MSI Mystic Light RGB lighting. With support for millions of colors and multiple lighting effects, you can create a personalized gaming setup that reflects your style. Sync your RGB lighting with other compatible devices using MSI Mystic Light Sync for an immersive gaming experience.</p>
                <h3>Easy Overclocking and System Tuning</h3>
                <p>Unlock the full potential of your hardware with MSIs intuitive BIOS interface and advanced overclocking features. With MSIs exclusive Core Boost technology and DDR5 Boost, you can easily overclock your CPU and memory for maximum performance without compromising stability.</p>
                <p>Elevate your gaming experience to the next level with the MSI Z790 GAMING PLUS WIFI motherboard. With its cutting-edge features, advanced technology, and robust design, this motherboard is the perfect choice for gamers who demand the best.</p>""",
                "sale_id": None,
            },
            {
            "id": 81,
            "name": "ASUS TUF GAMING B760-PLUS WIFI DDR4",
            "price": 156.0,
            "old_price": 178.0,
            "description": """<h3>ASUS TUF GAMING B760-PLUS WIFI DDR4: Built to Withstand the Rigors of Gaming</h3>
                <p>Designed for durability and performance, the ASUS TUF GAMING B760-PLUS WIFI DDR4 motherboard is the ideal choice for gamers seeking a reliable foundation for their gaming rig. Engineered with military-grade components and packed with gaming-centric features, this motherboard delivers stability, reliability, and seamless connectivity for an unparalleled gaming experience.</p>
                <h3>Military-Grade Durability</h3>
                <p>Featuring ASUS TUF components and TUF Protection, the TUF GAMING B760-PLUS WIFI DDR4 motherboard is built to withstand the rigors of gaming and overclocking. With enhanced ESD guards, TUF LANGuard, and overvoltage protection, this motherboard offers unmatched durability and reliability, ensuring long-term stability even under extreme conditions.</p>
                <h3>Powerful Performance</h3>
                <p>Powered by Intels latest B760 chipset, the TUF GAMING B760-PLUS WIFI DDR4 motherboard supports 12th generation Intel Core processors, providing exceptional performance for gaming, multitasking, and content creation. With support for DDR4 memory and PCIe 5.0 technology, this motherboard delivers blazing-fast speeds and responsive performance for the most demanding tasks.</p>
                <h3>High-Speed Connectivity</h3>
                <p>Stay connected with high-speed networking options on the TUF GAMING B760-PLUS WIFI DDR4 motherboard. Equipped with built-in WiFi 6E and Intel 2.5G LAN, this motherboard offers lightning-fast wireless and wired connectivity for lag-free online gaming and smooth streaming. Plus, with USB 3.2 Gen 2 ports, you can transfer data quickly and efficiently.</p>
                <h3>Immersive Gaming Audio</h3>
                <p>Experience immersive gaming audio with ASUS SupremeFX audio technology. Featuring Crystal Sound 3 and DTS:X Ultra, the TUF GAMING B760-PLUS WIFI DDR4 motherboard delivers crystal-clear sound with enhanced spatial awareness, allowing you to hear every detail in your favorite games.</p>
                <h3>Customizable RGB Lighting</h3>
                <p>Customize your gaming rig with ASUS Aura Sync RGB lighting. With a wide range of lighting effects and colors to choose from, you can create a personalized gaming setup that reflects your style. Sync your RGB lighting with other Aura Sync-compatible devices for a unified gaming experience.</p>
                <h3>Easy DIY Installation</h3>
                <p>With ASUS Q-LED indicators and Q-Slot and Q-DIMM slots, the TUF GAMING B760-PLUS WIFI DDR4 motherboard makes installation and upgrading easy and hassle-free. Plus, with ASUS BIOS Flashback and CrashFree BIOS 3, you can update your BIOS with ease and recover from system crashes quickly.</p>
                <p>Experience the ultimate gaming performance and reliability with the ASUS TUF GAMING B760-PLUS WIFI DDR4 motherboard. Built to withstand the rigors of gaming and packed with gaming-centric features, this motherboard is the perfect foundation for your gaming rig.</p>""",
            "sale_id": None,
        },
        {
            "id": 82,
            "name": "MSI MAG B550 TOMAHAWK WIFI",
            "price": 170.0,
            "old_price": 180.0,
            "description": """<h3>MSI MAG B550 TOMAHAWK WIFI: Power and Performance for Gaming Enthusiasts</h3>
                <p>Designed for gamers and PC enthusiasts, the MSI MAG B550 TOMAHAWK WIFI motherboard offers a perfect blend of power, performance, and reliability. With support for AMD Ryzen processors and a host of gaming-centric features, this motherboard provides a solid foundation for building a high-performance gaming PC.</p>
                <h3>Robust Power Delivery</h3>
                <p>The MAG B550 TOMAHAWK WIFI features an extended heatsink design with an extended PWM heatsink and enhanced circuit design to ensure stable power delivery to your components, even under heavy load. This robust power delivery system allows for overclocking and ensures reliable performance during intense gaming sessions.</p>
                <h3>Support for AMD Ryzen Processors</h3>
                <p>Compatible with AMD Ryzen processors, including Ryzen 5000 series CPUs, the MAG B550 TOMAHAWK WIFI motherboard offers exceptional performance for gaming, content creation, and multitasking. With support for PCIe 4.0 technology, you can take advantage of high-speed storage and graphics cards for a responsive gaming experience.</p>
                <h3>High-Speed Connectivity</h3>
                <p>Equipped with built-in WiFi 6 and 2.5G LAN, the MAG B550 TOMAHAWK WIFI provides lightning-fast wireless and wired networking options for lag-free gaming and smooth streaming. Plus, with USB 3.2 Gen 2 ports, you can transfer data quickly and easily between your devices.</p>
                <h3>Audio Boost Technology</h3>
                <p>Experience immersive gaming audio with MSI Audio Boost technology. Featuring high-quality audio components and Nahimic audio enhancer, the MAG B550 TOMAHAWK WIFI delivers crystal-clear sound with enhanced spatial awareness, allowing you to hear every detail in your favorite games.</p>
                <h3>Customizable RGB Lighting</h3>
                <p>Personalize your gaming rig with MSI Mystic Light RGB lighting. With customizable RGB headers and support for Mystic Light Sync, you can create stunning lighting effects and synchronize your lighting with other compatible devices for a truly immersive gaming experience.</p>
                <h3>Easy Installation and Setup</h3>
                <p>The MAG B550 TOMAHAWK WIFI features MSIs Click BIOS 5, which offers an intuitive interface for easy system configuration and overclocking. Plus, with MSI Dragon Center software, you can monitor system performance, adjust fan speeds, and customize RGB lighting from a single dashboard.</p>
                <p>With its powerful features, robust build quality, and gaming-centric design, the MSI MAG B550 TOMAHAWK WIFI motherboard is the perfect choice for gamers and PC enthusiasts looking to build a high-performance gaming PC.</p>""",
            "sale_id": None,
        },
        {
            "id": 83,
            "name": "Gigabyte B450 AORUS ELITE V2",
            "price": 56.0,
            "old_price": 78.0,
            "description": """<h3>Gigabyte B450 AORUS ELITE V2: Reliable Performance for Gaming and Productivity</h3>
                <p>The Gigabyte B450 AORUS ELITE V2 motherboard is designed to deliver reliable performance for gaming and productivity tasks. Built with high-quality components and featuring advanced technologies, this motherboard offers a solid foundation for your PC build.</p>
                <h3>Support for AMD Ryzen Processors</h3>
                <p>Compatible with AMD Ryzen processors, the B450 AORUS ELITE V2 motherboard provides excellent performance for gaming, content creation, and everyday computing tasks. With support for multi-core processing and overclocking capabilities, you can unleash the full potential of your CPU.</p>
                <h3>Robust Power Delivery</h3>
                <p>Equipped with an advanced power phase design and high-quality components, the B450 AORUS ELITE V2 ensures stable power delivery to your CPU and other components, even under heavy load. This helps to prevent overheating and ensures reliable performance during intense gaming sessions.</p>
                <h3>Enhanced Cooling Solutions</h3>
                <p>The B450 AORUS ELITE V2 features a comprehensive cooling system with multiple fan headers and advanced thermal management options. With support for aftermarket cooling solutions, you can keep your system cool and stable even during overclocking.</p>
                <h3>High-Speed Connectivity</h3>
                <p>Featuring PCIe Gen3 x4 M.2 slots and USB 3.1 Gen 2 ports, the B450 AORUS ELITE V2 offers high-speed connectivity options for ultra-fast data transfer and storage. With support for Gigabit LAN and onboard WiFi, you can enjoy smooth online gaming and streaming experiences.</p>
                <h3>Customizable RGB Lighting</h3>
                <p>Personalize your gaming rig with Gigabyte RGB Fusion 2.0. With customizable RGB lighting zones and support for digital LED strips, you can create stunning lighting effects to match your gaming setup. Sync your lighting with other compatible devices for a seamless gaming experience.</p>
                <h3>User-Friendly BIOS</h3>
                <p>The B450 AORUS ELITE V2 features Gigabytes award-winning BIOS interface, which offers easy access to advanced features and settings. With intuitive navigation and comprehensive system monitoring tools, you can fine-tune your system for optimal performance.</p>
                <p>Overall, the Gigabyte B450 AORUS ELITE V2 motherboard offers reliable performance, advanced features, and customizable options for gamers and PC enthusiasts alike. Whether youre building a gaming PC or a productivity workstation, this motherboard provides a solid foundation for your build.</p>""",
            "sale_id": None,
        },
        {
            "id": 84,
            "name": "ASUS ROG STRIX B550-F GAMING",
            "price": 130.0,
            "old_price": 150.0,
            "description": """<h3>ASUS ROG STRIX B550-F GAMING: Elevate Your Gaming Experience</h3>
                <p>The ASUS ROG STRIX B550-F GAMING motherboard is engineered to provide gamers with a premium gaming experience, offering a blend of performance, aesthetics, and advanced features. Built with high-quality components and designed for compatibility with the latest hardware, this motherboard is an excellent choice for gaming enthusiasts.</p>
                <h3>Powerful Performance for Gaming</h3>
                <p>Equipped with an AM4 socket and support for AMD Ryzen processors, the ROG STRIX B550-F GAMING delivers powerful performance for gaming and multitasking. With PCIe 4.0 support, high-speed DDR4 memory compatibility, and advanced cooling solutions, you can experience smooth and responsive gameplay even in demanding titles.</p>
                <h3>Robust Power Delivery</h3>
                <p>Featuring an optimized power design with high-quality components, the ROG STRIX B550-F GAMING ensures stable power delivery to your CPU and other components, allowing for reliable performance even under heavy load. This helps to prevent overheating and ensures consistent performance during extended gaming sessions.</p>
                <h3>Comprehensive Cooling Solutions</h3>
                <p>Designed with comprehensive cooling solutions, including multiple fan headers and heatsinks, the ROG STRIX B550-F GAMING helps to keep your system cool and stable even during intense gaming sessions. With support for liquid cooling solutions and customizable fan profiles, you can fine-tune your cooling performance to suit your needs.</p>
                <h3>Immersive Gaming Audio</h3>
                <p>Featuring ASUS SupremeFX audio technology, the ROG STRIX B550-F GAMING delivers immersive gaming audio with crystal-clear sound quality and precise positional audio cues. With support for high-fidelity audio codecs and advanced audio processing features, you can enjoy a competitive edge in your favorite games.</p>
                <h3>Personalized RGB Lighting</h3>
                <p>Express your style with customizable RGB lighting options on the ROG STRIX B550-F GAMING motherboard. With ASUS Aura Sync RGB lighting technology, you can synchronize your lighting effects with other compatible devices, creating a stunning visual experience that enhances your gaming setup.</p>
                <h3>User-Friendly BIOS Interface</h3>
                <p>The ROG STRIX B550-F GAMING features ASUS intuitive BIOS interface, which provides easy access to advanced features and settings. With comprehensive system monitoring tools and overclocking options, you can fine-tune your system for optimal performance and stability.</p>
                <p>Overall, the ASUS ROG STRIX B550-F GAMING motherboard offers gamers a premium gaming experience with its powerful performance, advanced features, and customizable options. Whether youre a casual gamer or a competitive esports player, this motherboard provides the performance and reliability you need to dominate the battlefield.</p>""",
            "sale_id": None,
        },
        {
            "id": 85,
            "name": "Gigabyte B550 AORUS ELITE V2",
            "price": 160.0,
            "old_price": 180.0,
            "description": """<h3>Gigabyte B550 AORUS ELITE V2: Elevate Your Gaming Rig</h3>
                <p>Experience next-level gaming performance with the Gigabyte B550 AORUS ELITE V2 motherboard. Designed to meet the demands of modern gamers and PC enthusiasts, this motherboard combines powerful features, advanced connectivity, and robust build quality to take your gaming experience to new heights.</p>
                <h3>Powerful Performance</h3>
                <p>The Gigabyte B550 AORUS ELITE V2 is equipped with an AM4 socket, providing compatibility with AMD Ryzen processors for unparalleled performance in gaming and multitasking. With support for PCIe 4.0 and high-speed DDR4 memory, you can enjoy smooth and responsive gameplay, even in the most demanding titles.</p>
                <h3>Advanced Cooling Solutions</h3>
                <p>Stay cool under pressure with the B550 AORUS ELITE V2s comprehensive cooling solutions. Featuring an advanced thermal design with multiple fan headers, heatsinks, and thermal pads, this motherboard ensures efficient heat dissipation to keep your system running smoothly, even during intense gaming sessions.</p>
                <h3>High-Speed Connectivity</h3>
                <p>Connectivity is key for gaming, and the B550 AORUS ELITE V2 delivers with high-speed networking options, including Gigabit Ethernet and PCIe 4.0 M.2 slots for ultra-fast storage. With USB 3.2 Gen 2 ports and support for the latest peripherals, you can enjoy seamless connectivity for all your gaming needs.</p>
                <h3>Immersive Audio Experience</h3>
                <p>Immerse yourself in the game with Gigabytes high-fidelity audio technology. The B550 AORUS ELITE V2 features an advanced audio chipset and premium audio capacitors, delivering crystal-clear sound quality and immersive gaming audio that brings your games to life.</p>
                <h3>RGB Fusion 2.0</h3>
                <p>Customize your gaming rig with Gigabytes RGB Fusion 2.0 technology. With customizable RGB lighting zones and effects, you can personalize your setup to match your style and create a gaming environment thats truly unique.</p>
                <h3>Easy-to-Use BIOS Interface</h3>
                <p>Access advanced features and settings with ease thanks to Gigabytes user-friendly BIOS interface. With intuitive controls and comprehensive system monitoring tools, you can optimize your system for maximum performance and stability.</p>
                <p>Overall, the Gigabyte B550 AORUS ELITE V2 motherboard offers gamers a powerful platform for building their dream gaming rig. With its advanced features, robust build quality, and sleek design, this motherboard is the perfect foundation for your gaming setup.</p>""",
            "sale_id": None,
        },
        {
            "id": 86,
            "name": "ASUS PRIME B550-PLUS",
            "price": 100.0,
            "old_price": 120.0,
            "description": """<h3>ASUS PRIME B550-PLUS: Your Gateway to Next-Gen Gaming</h3>
                <p>Experience the future of gaming with the ASUS PRIME B550-PLUS motherboard. Designed to deliver exceptional performance, reliability, and versatility, this motherboard is the perfect foundation for your gaming rig.</p>
                <h3>Powerful Performance</h3>
                <p>The ASUS PRIME B550-PLUS features an AM4 socket, providing compatibility with the latest AMD Ryzen processors. With PCIe 4.0 support and high-speed DDR4 memory, you can enjoy blazing-fast speeds and responsive performance in all your favorite games.</p>
                <h3>Comprehensive Connectivity</h3>
                <p>Connectivity is key for gaming, and the PRIME B550-PLUS has you covered. With dual M.2 slots, USB 3.2 Gen 2 ports, and Gigabit Ethernet, you can enjoy lightning-fast data transfer speeds and lag-free online gaming.</p>
                <h3>AI Noise-Canceling Microphone</h3>
                <p>Communicate clearly with your teammates using the built-in AI noise-canceling microphone. This innovative feature reduces background noise and enhances voice clarity, ensuring crystal-clear communication in-game and during video calls.</p>
                <h3>ASUS Aura Sync</h3>
                <p>Customize your gaming setup with ASUS Aura Sync RGB lighting. With a wide range of compatible RGB components and accessories, you can create stunning lighting effects that sync with your gameplay and reflect your personal style.</p>
                <h3>Comprehensive Cooling Solutions</h3>
                <p>Keep your system cool under pressure with the PRIME B550-PLUSs comprehensive cooling solutions. With multiple fan headers, heatsinks, and thermal pads, this motherboard ensures efficient heat dissipation to maintain optimal performance even during intense gaming sessions.</p>
                <h3>Enhanced Audio Experience</h3>
                <p>Immerse yourself in the game with ASUS audio enhancements. The PRIME B550-PLUS features high-fidelity audio components and advanced audio processing technologies, delivering immersive sound quality that brings your games to life.</p>
                <h3>User-Friendly BIOS Interface</h3>
                <p>Take control of your system with the intuitive BIOS interface. With easy-to-use controls and comprehensive system monitoring tools, you can optimize your system settings for maximum performance and stability.</p>
                <p>Overall, the ASUS PRIME B550-PLUS motherboard offers gamers a powerful platform for building their dream gaming rig. With its advanced features, reliable performance, and sleek design, this motherboard is the perfect choice for gamers looking to take their gaming experience to the next level.</p>""",
            "sale_id": None,
        },
        {
            "id": 87,
            "name": "MSI MAG 650W 80 Plus Bronze",
            "price": 100.0,
            "old_price": 120.0,
            "description": """<h2>MSI MAG 650W 80 Plus Bronze Power Supply</h2>
                <p>The MSI MAG 650W power supply is designed to deliver reliable and efficient power to your gaming PC. With its 80 Plus Bronze certification, robust build quality, and advanced features, it provides the performance and stability you need for intense gaming sessions and demanding workloads.</p>
                <h2>Efficient Power Delivery</h2>
                <p>Featuring an 80 Plus Bronze certification, the MSI MAG 650W power supply delivers up to 85% energy efficiency, ensuring stable and reliable power delivery to your system components. This efficiency rating helps reduce energy waste and heat generation, resulting in lower electricity bills and cooler operation.</p>
                <h2>Robust Build Quality</h2>
                <p>Constructed with high-quality components and advanced engineering, the MSI MAG 650W power supply offers excellent reliability and durability. Its robust design and strict quality control measures ensure long-term performance and stability, even under heavy loads and extreme conditions.</p>
                <h2>Quiet Operation</h2>
                <p>The MSI MAG 650W power supply features a silent 120mm fan with optimized blade design and advanced airflow technology. This fan operates quietly while providing efficient cooling, ensuring optimal thermal performance without generating excessive noise.</p>
                <h2>Modular Design</h2>
                <p>Equipped with a modular cable design, the MSI MAG 650W power supply allows you to connect only the cables you need, reducing clutter and improving airflow inside your PC case. This modular design not only simplifies cable management but also enhances the overall aesthetics of your build.</p>
                <h2>Comprehensive Protection Features</h2>
                <p>The MSI MAG 650W power supply is equipped with comprehensive protection features to safeguard your components against various electrical hazards. These include over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP).</p>
                <h2>Compatibility and Connectivity</h2>
                <p>With its ATX form factor and standard connectors, the MSI MAG 650W power supply is compatible with most modern PC cases and motherboards. It comes with a variety of connectors, including 24-pin ATX, 8-pin EPS, PCIe, SATA, and peripheral connectors, ensuring broad compatibility with a wide range of hardware configurations.</p>
                <h2>Conclusion</h2>
                <p>The MSI MAG 650W power supply offers reliable performance, efficient power delivery, and advanced features to meet the demands of gaming enthusiasts and PC builders. With its 80 Plus Bronze certification, robust build quality, quiet operation, modular design, comprehensive protection features, and broad compatibility, it provides a solid foundation for your gaming rig or workstation.</p>""",
            "sale_id": None,
        },
        {
            "id": 88,
            "name": "ENDORFY Supremo FM5 1000W 80 Plus Gold",
            "price": 125.0,
            "old_price": 130.0,
            "description": """<h2>ENDORFY Supremo FM5 1000W 80 Plus Gold Power Supply</h2>
                <p>The ENDORFY Supremo FM5 1000W power supply is designed to deliver reliable and efficient power to high-performance gaming rigs and workstations. With its 80 Plus Gold certification, advanced features, and robust build quality, it provides the performance and stability needed for demanding applications.</p>
                <h2>Efficient Power Delivery</h2>
                <p>Featuring an 80 Plus Gold certification, the ENDORFY Supremo FM5 1000W power supply offers up to 90% energy efficiency, ensuring stable and efficient power delivery to your system components. This high efficiency rating reduces energy waste, lowers operating costs, and minimizes heat generation.</p>
                <h2>Robust Build Quality</h2>
                <p>The ENDORFY Supremo FM5 1000W power supply is built with premium components and undergoes rigorous quality control testing to ensure long-term reliability and durability. Its robust design and high-quality construction make it suitable for high-end gaming setups and professional workstations.</p>
                <h2>Quiet Operation</h2>
                <p>Equipped with a silent 140mm fan with optimized blade design and hydraulic bearings, the ENDORFY Supremo FM5 1000W power supply operates quietly while providing efficient cooling. This ensures optimal thermal performance without generating excessive noise, even under heavy loads.</p>
                <h2>Modular Design</h2>
                <p>The ENDORFY Supremo FM5 1000W power supply features a modular cable design, allowing you to connect only the cables you need for your specific configuration. This not only simplifies cable management but also improves airflow inside your PC case, resulting in better overall system cooling.</p>
                <h2>Comprehensive Protection Features</h2>
                <p>Designed with comprehensive protection features, the ENDORFY Supremo FM5 1000W power supply safeguards your components against various electrical hazards. These include over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP).</p>
                <h2>Compatibility and Connectivity</h2>
                <p>With its ATX form factor and standard connectors, the ENDORFY Supremo FM5 1000W power supply is compatible with most PC cases and motherboards on the market. It comes with a variety of connectors, including 24-pin ATX, 8-pin EPS, PCIe, SATA, and peripheral connectors, ensuring broad compatibility with a wide range of hardware configurations.</p>
                <h2>Conclusion</h2>
                <p>The ENDORFY Supremo FM5 1000W power supply offers high efficiency, reliable performance, and advanced features for demanding gaming and workstation setups. With its 80 Plus Gold certification, robust build quality, quiet operation, modular design, comprehensive protection features, and broad compatibility, it provides a solid foundation for building a powerful and stable PC system.</p>""",
            "sale_id": 7,
        },
        {
            "id": 89,
            "name": "Thermaltake Litepower II Black 550W",
            "price": 80.0,
            "old_price": 70.0,
            "description": """<h2>Thermaltake Litepower II Black 550W Power Supply</h2>
                <p>The Thermaltake Litepower II Black 550W power supply is a reliable and efficient solution for powering your desktop computer. With its stable performance, high-quality components, and sleek design, it provides the essential power your system needs for everyday computing tasks.</p>
                <h2>Stable and Reliable Performance</h2>
                <p>Equipped with a single +12V rail design, the Thermaltake Litepower II Black 550W power supply delivers stable and reliable power to your system components, ensuring smooth operation and consistent performance. This makes it suitable for basic computing tasks, multimedia entertainment, and light gaming.</p>
                <h2>High-Quality Components</h2>
                <p>The Thermaltake Litepower II Black 550W power supply features high-quality components, including Japanese capacitors, which provide reliable power delivery and long-term durability. These premium components contribute to the power supplys overall reliability and help extend its lifespan.</p>
                <h2>Sleek Design</h2>
                <p>With its sleek black casing and minimalist design, the Thermaltake Litepower II Black 550W power supply complements any PC build, adding a touch of elegance to your system. Its compact form factor and black finish make it blend seamlessly into most computer cases, while the subtle branding adds a touch of style.</p>
                <h2>Quiet Operation</h2>
                <p>The Thermaltake Litepower II Black 550W power supply features a quiet 120mm cooling fan that effectively dissipates heat while keeping noise levels to a minimum. This ensures quiet operation even during extended use, allowing you to focus on your work or enjoy multimedia content without distraction.</p>
                <h2>Comprehensive Protection Features</h2>
                <p>Designed with comprehensive protection features, the Thermaltake Litepower II Black 550W power supply safeguards your components against various electrical hazards. These include over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP).</p>
                <h2>Wide Compatibility</h2>
                <p>With its standard ATX form factor and universal connectors, the Thermaltake Litepower II Black 550W power supply is compatible with a wide range of desktop computer systems. It comes with all the necessary cables and connectors, including 24-pin ATX, 4+4-pin EPS, PCIe, SATA, and peripheral connectors, ensuring broad compatibility with different hardware configurations.</p>
                <h2>Conclusion</h2>
                <p>The Thermaltake Litepower II Black 550W power supply offers stable performance, high-quality components, and a sleek design, making it a reliable and efficient choice for powering your desktop computer. Whether youre building a new system or upgrading an existing one, the Litepower II Black 550W power supply provides the essential power your components need to operate smoothly.</p>""",
            "sale_id": None,
        },
        {
            "id": 90,
            "name": "Seasonic Prime TX 1000W 80 Plus Titanium",
            "price": 400.0,
            "old_price": 420.0,
            "description": """<h2>Seasonic Prime TX 1000W 80 Plus Titanium Power Supply</h2>
                <p>The Seasonic Prime TX 1000W power supply is a high-performance and energy-efficient solution designed to meet the demanding needs of modern gaming rigs and workstation setups. With its 80 Plus Titanium certification, advanced design, and robust construction, it offers exceptional reliability, efficiency, and stability for your PC build.</p>
                <h2>Efficient Power Delivery</h2>
                <p>Featuring an 80 Plus Titanium certification, the Seasonic Prime TX 1000W power supply delivers exceptional energy efficiency, with up to 94% efficiency at typical load conditions. This means less wasted energy, reduced heat output, and lower electricity bills, making it an environmentally friendly choice for your system.</p>
                <h2>High-Performance Components</h2>
                <p>The Seasonic Prime TX 1000W power supply is built with high-quality components, including premium Japanese capacitors, which ensure stable and reliable power delivery under demanding conditions. The use of high-performance components also contributes to the power supplys long-term durability and reliability.</p>
                <h2>Modular Design</h2>
                <p>Featuring a fully modular design, the Seasonic Prime TX 1000W power supply allows you to connect only the cables you need for your system, reducing cable clutter and improving airflow inside your PC case. This makes cable management easier and helps create a cleaner and more organized build.</p>
                <h2>Hybrid Fan Control</h2>
                <p>The Seasonic Prime TX 1000W power supply features a hybrid fan control system that automatically adjusts fan speed according to system load and temperature. Under low to moderate loads, the fan operates silently in fanless mode, ensuring quiet operation during everyday use. When the system is under heavy load, the fan ramps up to provide optimal cooling performance.</p>
                <h2>Comprehensive Protection Features</h2>
                <p>Equipped with comprehensive protection features, including over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP), the Seasonic Prime TX 1000W power supply safeguards your components against various electrical hazards, ensuring reliable operation and peace of mind.</p>
                <h2>Compact and Durable Design</h2>
                <p>With its compact form factor and durable construction, the Seasonic Prime TX 1000W power supply is designed to fit seamlessly into most PC cases while withstanding the rigors of daily use. Its sleek and understated design makes it a stylish addition to any build, while its robust build quality ensures long-term reliability.</p>
                <h2>Conclusion</h2>
                <p>The Seasonic Prime TX 1000W power supply offers exceptional performance, efficiency, and reliability, making it an ideal choice for high-end gaming PCs, workstations, and enthusiast builds. With its 80 Plus Titanium certification, modular design, and comprehensive protection features, it provides the power and stability your system needs to excel in demanding applications.</p>""",
            "sale_id": None,
        },
        {
            "id": 91,
            "name": "Seasonic FOCUS SPX 750W 80 Plus Platinum",
            "price": 200.0,
            "old_price": 220.0,
            "description": """<h2>Seasonic FOCUS SPX 750W 80 Plus Platinum Power Supply</h2>
                <p>The Seasonic FOCUS SPX 750W power supply is a high-quality and efficient solution designed to meet the demanding power requirements of modern PC systems. With its 80 Plus Platinum certification, advanced features, and reliable performance, it delivers stable and clean power to your components, ensuring optimal performance and efficiency.</p>
                <h2>Efficiency and Performance</h2>
                <p>With its 80 Plus Platinum certification, the Seasonic FOCUS SPX 750W power supply achieves up to 92% energy efficiency at typical load conditions. This high level of efficiency reduces wasted energy and helps lower electricity bills, making it an environmentally friendly choice for your system.</p>
                <h2>Modular Design</h2>
                <p>The Seasonic FOCUS SPX 750W power supply features a fully modular design, allowing you to connect only the cables you need for your build. This modular design reduces cable clutter inside your case, improves airflow, and makes cable management easier, resulting in a cleaner and more organized build.</p>
                <h2>Silent Operation</h2>
                <p>Equipped with a silent 120mm fan with a Fluid Dynamic Bearing (FDB), the Seasonic FOCUS SPX 750W power supply operates quietly even under heavy loads. The fans optimized blade design and low noise profile ensure silent operation, allowing you to focus on your work or gaming without distraction.</p>
                <h2>Advanced Protection Features</h2>
                <p>The Seasonic FOCUS SPX 750W power supply is equipped with advanced protection features to safeguard your components against electrical hazards. These include over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP), ensuring reliable operation and peace of mind.</p>
                <h2>Compact and Reliable Design</h2>
                <p>With its compact form factor and reliable build quality, the Seasonic FOCUS SPX 750W power supply is designed to fit seamlessly into most PC cases while providing long-term reliability. Its durable construction and high-quality components ensure stable and consistent power delivery, even under demanding conditions.</p>
                <h2>Conclusion</h2>
                <p>The Seasonic FOCUS SPX 750W power supply offers high efficiency, reliable performance, and silent operation, making it an ideal choice for gaming PCs, workstations, and other high-performance systems. With its modular design, advanced protection features, and compact form factor, it provides the power and stability your system needs to excel in any task.</p>""",
            "sale_id": None,
        },
        {
            "id": 92,
            "name": "Cooler Master MWE GOLD-V2 750W 80 Plus Gold",
            "price": 105.0,
            "old_price": 120.0,
            "description": """<h2>Cooler Master MWE GOLD-V2 750W 80 Plus Gold Power Supply</h2>
                <p>The Cooler Master MWE GOLD-V2 750W power supply is a reliable and efficient solution designed to meet the demanding power requirements of modern PC systems. With its 80 Plus Gold certification, advanced features, and stable performance, it delivers clean and efficient power to your components, ensuring reliable operation and optimal performance.</p>
                <h2>Efficiency and Performance</h2>
                <p>With its 80 Plus Gold certification, the Cooler Master MWE GOLD-V2 750W power supply achieves up to 90% energy efficiency at typical load conditions. This high level of efficiency reduces energy waste and helps lower electricity bills, making it a cost-effective choice for your system.</p>
                <h2>Modular Design</h2>
                <p>The Cooler Master MWE GOLD-V2 750W power supply features a fully modular design, allowing you to connect only the cables you need for your build. This modular design reduces cable clutter inside your case, improves airflow, and makes cable management easier, resulting in a cleaner and more organized build.</p>
                <h2>Silent Operation</h2>
                <p>Equipped with a silent 120mm fan with a LDB (Loop Dynamic Bearing), the Cooler Master MWE GOLD-V2 750W power supply operates quietly even under heavy loads. The fans optimized blade design and low noise profile ensure silent operation, allowing you to focus on your work or gaming without distraction.</p>
                <h2>Advanced Protection Features</h2>
                <p>The Cooler Master MWE GOLD-V2 750W power supply is equipped with advanced protection features to safeguard your components against electrical hazards. These include over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP), ensuring reliable operation and peace of mind.</p>
                <h2>Compact and Reliable Design</h2>
                <p>With its compact form factor and reliable build quality, the Cooler Master MWE GOLD-V2 750W power supply is designed to fit seamlessly into most PC cases while providing long-term reliability. Its durable construction and high-quality components ensure stable and consistent power delivery, even under demanding conditions.</p>
                <h2>Conclusion</h2>
                <p>The Cooler Master MWE GOLD-V2 750W power supply offers high efficiency, reliable performance, and silent operation, making it an ideal choice for gaming PCs, workstations, and other high-performance systems. With its modular design, advanced protection features, and compact form factor, it provides the power and stability your system needs to excel in any task.</p>""",
            "sale_id": None,
        },
        {
            "id": 93,
            "name": "NZXT C1200 V2 1200W 80 Plus Gold",
            "price": 300.0,
            "old_price": 320.0,
            "description": """<h2>NZXT C1200 V2 1200W 80 Plus Gold Power Supply</h2>
                <p>The NZXT C1200 V2 1200W power supply is a high-performance unit designed to meet the demanding power requirements of enthusiast PC builds. With its 80 Plus Gold certification, robust construction, and advanced features, it delivers reliable and efficient power to your components, ensuring stable performance under heavy loads.</p>
                <h2>Efficiency and Certification</h2>
                <p>The NZXT C1200 V2 power supply boasts an 80 Plus Gold certification, which guarantees high energy efficiency of up to 90% at typical load conditions. This ensures that less energy is wasted as heat, reducing your electricity bill and minimizing environmental impact.</p>
                <h2>Modular Design</h2>
                <p>Featuring a fully modular design, the NZXT C1200 V2 allows you to connect only the cables you need for your system, reducing clutter and improving airflow inside your case. This modular design not only enhances the aesthetics of your build but also makes cable management easier and more efficient.</p>
                <h2>Smart Fan Control</h2>
                <p>The NZXT C1200 V2 is equipped with a smart fan control system that adjusts fan speed according to load and temperature, ensuring optimal cooling performance while minimizing noise. This allows for silent operation during low to moderate loads and ensures that the power supply remains cool and stable under heavy loads.</p>
                <h2>Advanced Protection Features</h2>
                <p>Designed with safety in mind, the NZXT C1200 V2 incorporates various protection features to safeguard your components from electrical hazards. These include over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP), ensuring reliable operation and peace of mind.</p>
                <h2>Compact and Durable Construction</h2>
                <p>The NZXT C1200 V2 features a compact and durable construction that fits seamlessly into most PC cases while providing long-term reliability. Its high-quality components and robust design ensure stable power delivery and consistent performance, even under demanding conditions.</p>
                <h2>Conclusion</h2>
                <p>The NZXT C1200 V2 1200W power supply offers high efficiency, modular design, and advanced protection features, making it an ideal choice for enthusiast PC builds. With its reliable performance, smart fan control, and compact form factor, it provides the power and stability needed to support high-performance components and demanding tasks.</p>""",
            "sale_id": None,
        },
        {
            "id": 94,
            "name": "KRUX Generator 850W 80 Plus Gold",
            "price": 120.0,
            "old_price": 125.0,
            "description": """<h2>KRUX Generator 850W 80 Plus Gold Power Supply</h2>
                <p>The KRUX Generator 850W power supply is a high-quality unit designed to meet the power demands of gaming PCs and enthusiast builds. With its 80 Plus Gold certification, advanced features, and robust construction, it delivers efficient and reliable power to your components, ensuring stable performance under heavy loads.</p>
                <h2>Efficiency and Certification</h2>
                <p>The KRUX Generator 850W power supply boasts an 80 Plus Gold certification, indicating high energy efficiency of up to 90% at typical load conditions. This certification ensures that the power supply operates with minimal wasted energy, reducing electricity costs and environmental impact.</p>
                <h2>Modular Design</h2>
                <p>Featuring a modular cable design, the KRUX Generator 850W allows you to connect only the cables you need for your system, reducing cable clutter and improving airflow inside your PC case. This modular design not only enhances the aesthetics of your build but also simplifies cable management, making installation easier and more efficient.</p>
                <h2>Smart Cooling System</h2>
                <p>The KRUX Generator 850W is equipped with a smart cooling system that automatically adjusts fan speed based on temperature and load, ensuring optimal cooling performance while minimizing noise levels. This intelligent fan control mechanism ensures quiet operation during normal use and provides additional cooling when needed under heavy loads.</p>
                <h2>Comprehensive Protection Features</h2>
                <p>Designed to protect your components from electrical hazards, the KRUX Generator 850W incorporates a range of advanced protection features. These include over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP), ensuring reliable operation and safeguarding your hardware investment.</p>
                <h2>Durable Construction</h2>
                <p>The KRUX Generator 850W power supply features a durable construction with high-quality components, ensuring long-term reliability and stability. Its robust design and efficient cooling system allow for continuous operation under demanding conditions, making it suitable for gaming, content creation, and other intensive tasks.</p>
                <h2>Conclusion</h2>
                <p>The KRUX Generator 850W 80 Plus Gold power supply offers high efficiency, modular design, and comprehensive protection features, making it an excellent choice for gaming PCs and enthusiast builds. With its reliable performance, smart cooling system, and durable construction, it provides the power and stability needed to support high-performance components and demanding applications.</p>""",
            "sale_id": None,
        },
        {
            "id": 95,
            "name": "Seasonic Focus GX 750W 80 Plus Gold",
            "price": 50.0,
            "old_price": 70.0,
            "description": """<h2>Seasonic Focus GX 750W 80 Plus Gold Power Supply</h2>
                <p>The Seasonic Focus GX 750W power supply is a high-quality unit designed to meet the demanding power requirements of gaming PCs, workstations, and enthusiast builds. With its 80 Plus Gold certification, advanced features, and reliable performance, it delivers efficient and stable power to your components, ensuring smooth operation even under heavy loads.</p>
                <h2>Efficiency and Certification</h2>
                <p>The Seasonic Focus GX 750W power supply boasts an 80 Plus Gold certification, indicating high energy efficiency of up to 90% at typical load conditions. This certification ensures that the power supply operates with minimal wasted energy, reducing electricity costs and environmental impact.</p>
                <h2>Modular Design</h2>
                <p>Featuring a fully modular cable design, the Seasonic Focus GX 750W allows you to connect only the cables you need for your system, reducing cable clutter and improving airflow inside your PC case. This modular design not only enhances the aesthetics of your build but also simplifies cable management, making installation easier and more efficient.</p>
                <h2>Hybrid Silent Fan Control</h2>
                <p>The Seasonic Focus GX 750W features a hybrid silent fan control system that automatically adjusts fan speed based on temperature and load, ensuring optimal cooling performance while minimizing noise levels. This intelligent fan control mechanism ensures quiet operation during normal use and provides additional cooling when needed under heavy loads.</p>
                <h2>Comprehensive Protection Features</h2>
                <p>Designed to protect your components from electrical hazards, the Seasonic Focus GX 750W incorporates a range of advanced protection features. These include over-voltage protection (OVP), under-voltage protection (UVP), over-power protection (OPP), short-circuit protection (SCP), and over-temperature protection (OTP), ensuring reliable operation and safeguarding your hardware investment.</p>
                <h2>Compact Size and High Build Quality</h2>
                <p>The Seasonic Focus GX 750W power supply features a compact size and high build quality, making it suitable for a wide range of PC builds. Its durable construction, premium components, and rigorous testing ensure long-term reliability and stability, making it an ideal choice for gaming, content creation, and other demanding applications.</p>
                <h2>Conclusion</h2>
                <p>The Seasonic Focus GX 750W 80 Plus Gold power supply offers high efficiency, modular design, and comprehensive protection features, making it an excellent choice for gaming PCs, workstations, and enthusiast builds. With its reliable performance, silent fan control, and compact size, it provides the power and stability needed to support high-performance components and demanding tasks.</p>""",
            "sale_id": None,
        },
        {
            "id": 96,
            "name": "AMD Ryzen 9 7900X",
            "price": 400.0,
            "old_price": 500.0,
            "description": """<h2>Unleash Unprecedented Power</h2>
                <p>Prepare to experience the pinnacle of computing performance with the AMD Ryzen 9 7900X processor. Featuring advanced Zen 4 architecture and cutting-edge manufacturing technology, this CPU redefines whats possible in gaming, content creation, and multitasking.</p>
                <h2>Dominate Every Task</h2>
                <p>With a whopping 16 high-performance cores and 32 threads, the Ryzen 9 7900X delivers unrivaled processing power to tackle even the most demanding workloads with ease. Whether youre rendering complex 3D scenes, editing high-resolution videos, or streaming your gameplay, this processor ensures smooth performance and responsiveness.</p>
                <h2>Next-Level Performance</h2>
                <p>Equipped with AMDs latest technologies, including Precision Boost 3 and Infinity Cache, the Ryzen 9 7900X offers blistering-fast clock speeds and reduced memory latency for a performance boost in gaming and multitasking sPRICErios. Say goodbye to bottlenecks and hello to seamless computing.</p>
                <h2>Efficiency Meets Power</h2>
                <p>Despite its incredible performance capabilities, the Ryzen 9 7900X remains energy-efficient thanks to AMDs advanced power management features. With support for PCIe 5.0 and DDR5 memory, it offers lightning-fast data transfer speeds for snappier system responsiveness and smoother overall performance.</p>
                <h2>Unrivaled Versatility</h2>
                <p>Whether youre a hardcore gamer, a professional content creator, or a multitasking powerhouse, the AMD Ryzen 9 7900X empowers you to achieve more than ever before. Dominate your competition, unleash your creativity, and elevate your computing experience to new heights with this exceptional CPU.</p>""",
            "sale_id": None,
        },
        {
            "id": 97,
            "name": "AMD Ryzen 7 7800X3D",
            "price": 332.0,
            "old_price": 345.0,
            "description": """<h2>Experience Next-Gen Performance</h2>
                <p>Step into the future of computing with the AMD Ryzen 7 7800X3D processor. Built on the cutting-edge Zen 4 architecture and fabricated using the latest manufacturing processes, this CPU delivers unparalleled performance for gaming, content creation, and multitasking.</p>
                <h2>Unleash Your Creativity</h2>
                <p>With 8 high-performance cores and 16 threads, the Ryzen 7 7800X3D offers lightning-fast processing power to handle even the most demanding tasks with ease. Whether youre editing videos, rendering 3D graphics, or streaming gameplay, this processor ensures smooth performance and responsiveness.</p>
                <h2>Revolutionary 3D V-Cache Technology</h2>
                <p>Equipped with revolutionary 3D V-Cache technology, the Ryzen 7 7800X3D pushes the boundaries of CPU performance. By stacking an extra layer of cache directly on the CPU die, it significantly enhances gaming performance, reducing latency and improving frame rates for a more immersive gaming experience.</p>
                <h2>Efficiency Redefined</h2>
                <p>Despite its incredible power, the Ryzen 7 7800X3D remains energy-efficient thanks to AMDs advanced power management technologies. With support for PCIe 4.0 and DDR5 memory, it offers blazing-fast data transfer speeds for faster loading times and smoother overall system performance.</p>
                <h2>Unlock Your Potential</h2>
                <p>Whether youre a hardcore gamer, a creative professional, or a multitasking enthusiast, the AMD Ryzen 7 7800X3D unlocks new levels of performance and productivity. Dominate your competition and take your computing experience to the next level with this powerhouse CPU.</p>""",
            "sale_id": None,
        },
        {
            "id": 98,
            "name": "AMD Ryzen 5 5600",
            "price": 120.0,
            "old_price": 140.0,
            "description": """<h2>Unleash Exceptional Performance</h2>
                <p>Experience the perfect blend of power and efficiency with the AMD Ryzen 5 5600 processor. Built on the revolutionary Zen 3 architecture and crafted with cutting-edge 7nm technology, this CPU delivers unparalleled performance for gaming, productivity, and beyond.</p>
                <h2>Seamless Multitasking</h2>
                <p>With 6 cores and 12 threads, the Ryzen 5 5600 is engineered to handle multitasking with ease. Whether youre streaming, gaming, or tackling productivity tasks, this processor delivers smooth and responsive performance, allowing you to effortlessly switch between applications without missing a beat.</p>
                <h2>Boost Your Gaming Experience</h2>
                <p>Equipped with AMDs Precision Boost 2 technology, the Ryzen 5 5600 dynamically adjusts clock speeds to optimize performance in gaming sPRICErios. Combined with support for PCIe 4.0 and fast DDR4 memory, youll enjoy lightning-fast load times, immersive gameplay, and fluid frame rates.</p>
                <h2>Efficiency Redefined</h2>
                <p>Despite its formidable performance capabilities, the Ryzen 5 5600 remains energy-efficient, thanks to its advanced power management features. With lower power consumption and reduced heat output, this processor offers a cooler and quieter computing experience without compromising on performance.</p>
                <h2>Unlock Your Potential</h2>
                <p>Whether youre a gamer, content creator, or power user, the AMD Ryzen 5 5600 unlocks new levels of performance and versatility. Elevate your computing experience, unleash your creativity, and conquer every task with confidence with this exceptional CPU at the heart of your system.</p>""",
            "sale_id": None,
        },
        {
            "id": 99,
            "name": "AMD Ryzen 5 7600X",
            "price": 190.0,
            "old_price": 200.0,
            "description": """<h2>Unleash Unrivaled Performance</h2>
                <p>Introducing the AMD Ryzen 5 7600X, a powerhouse processor designed to revolutionize your computing experience. Built on the innovative Zen 3 architecture and engineered with cutting-edge 7nm technology, this CPU delivers exceptional performance and efficiency for gaming, content creation, and multitasking.</p>
                <h2>Effortless Multitasking</h2>
                <p>With 8 cores and 16 threads, the Ryzen 5 7600X is engineered to handle demanding multitasking sPRICErios with ease. Seamlessly switch between applications, stream, edit videos, and tackle heavy workloads without sacrificing performance or responsiveness.</p>
                <h2>Elevate Your Gaming Experience</h2>
                <p>Equipped with AMDs Precision Boost 2 technology, the Ryzen 5 7600X dynamically adjusts clock speeds to deliver optimal performance in gaming environments. Paired with support for PCIe 4.0 and high-speed DDR4 memory, this processor ensures smooth gameplay, faster load times, and immersive visuals.</p>
                <h2>Efficiency Meets Power</h2>
                <p>Despite its incredible performance capabilities, the Ryzen 5 7600X remains energy-efficient, thanks to advanced power management features. Experience lower power consumption and reduced heat output, allowing for quieter operation and cooler temperatures even during intense gaming sessions.</p>
                <h2>Unleash Your Creativity</h2>
                <p>Whether youre a gamer, content creator, or power user, the AMD Ryzen 5 7600X empowers you to unleash your creativity and achieve more. Elevate your productivity, unlock new gaming horizons, and conquer every task with confidence with this exceptional CPU powering your system.</p>""",
            "sale_id": None,
        },
        {
            "id": 100,
            "name": "AMD Ryzen 5 8600G",
            "price": 210.0,
            "old_price": 270.0,
            "description": """<h2>Unleash Exceptional Performance</h2>
                <p>Introducing the AMD Ryzen 5 8600G, a powerful processor engineered to redefine your computing experience. Built on the innovative Zen 3 architecture and crafted with cutting-edge 7nm technology, this CPU delivers unparalleled performance and efficiency for gaming, content creation, and multitasking.</p>
                <h2>Seamless Multitasking</h2>
                <p>Featuring 6 cores and 12 threads, the Ryzen 5 8600G is designed to effortlessly handle demanding multitasking sPRICErios. Switch between applications, stream content, edit videos, and tackle intensive workloads with ease, all without compromising on performance or responsiveness.</p>
                <h2>Elevate Your Gaming</h2>
                <p>Equipped with AMDs Precision Boost 2 technology, the Ryzen 5 8600G dynamically adjusts clock speeds to deliver optimal gaming performance. With support for PCIe 4.0 and high-speed DDR4 memory, experience smooth gameplay, reduced loading times, and stunning visuals that immerse you in your favorite games.</p>
                <h2>Efficiency and Power</h2>
                <p>Despite its impressive performance capabilities, the Ryzen 5 8600G remains energy-efficient, thanks to advanced power management features. Experience lower power consumption and reduced heat output, ensuring quieter operation and cooler temperatures even during intense gaming sessions.</p>
                <h2>Unleash Your Creativity</h2>
                <p>Whether youre a gamer, content creator, or power user, the AMD Ryzen 5 8600G empowers you to unleash your creativity and achieve more. Boost your productivity, unlock new gaming possibilities, and conquer every task with confidence, knowing that this exceptional CPU is driving your system forward.</p>""",
            "sale_id": None,
        },
        {
            "id": 101,
            "name": "Intel Core i5-13400F",
            "price": 150.0,
            "old_price": 170.0,
            "description": """<h2>Next-Level Performance</h2>
                <p>Meet the Intel Core i5-13400F, a powerhouse processor designed to take your computing experience to the next level. Built on Intels advanced 12th generation Alder Lake architecture, this CPU delivers exceptional performance and responsiveness for gaming, productivity, and multitasking.</p>
                <h2>Efficient Multithreading</h2>
                <p>With 6 cores and 12 threads, the Core i5-13400F offers impressive multitasking capabilities, allowing you to effortlessly handle demanding workloads and applications. Experience smooth performance whether youre gaming, streaming, editing videos, or running multiple tasks simultaneously.</p>
                <h2>Boosted Gaming Experience</h2>
                <p>Equipped with Intel Turbo Boost Max Technology 3.0, the Core i5-13400F automatically increases clock speeds to deliver enhanced gaming performance when you need it most. Enjoy faster frame rates, reduced input lag, and smoother gameplay for an immersive gaming experience.</p>
                <h2>Enhanced Connectivity</h2>
                <p>Featuring PCIe Gen 5 and DDR5 memory support, the Core i5-13400F ensures lightning-fast data transfer speeds and improved system responsiveness. Connect high-speed peripherals, upgrade to the latest memory technology, and unlock new levels of performance for your gaming rig.</p>
                <h2>Intelligent Power Management</h2>
                <p>With Intels Enhanced SpeedStep and Deep Sleep technologies, the Core i5-13400F optimizes power efficiency without sacrificing performance. Enjoy longer battery life on laptops and lower power consumption on desktops, ensuring a greener computing experience.</p>
                <h2>Unleash Your Creativity</h2>
                <p>Whether youre a gamer, content creator, or everyday user, the Intel Core i5-13400F empowers you to unleash your creativity and achieve more. From gaming to content creation and everything in between, this powerful CPU enables you to do it all with ease.</p>""",
            "sale_id": None,
        },
        {
            "id": 102,
            "name": "Intel Core i9-13900KF",
            "price": 500.0,
            "old_price": 700.0,
            "description": """<h2>Unmatched Performance</h2>
                <p>Introducing the Intel Core i9-13900KF, a high-performance processor designed to push the boundaries of computing. Built on Intels cutting-edge 12th generation Alder Lake architecture, this CPU delivers unparalleled performance for gaming, content creation, and heavy multitasking.</p>
                <h2>Exceptional Multithreading</h2>
                <p>With 12 cores and 24 threads, the Core i9-13900KF offers exceptional multithreading capabilities, allowing you to breeze through demanding tasks with ease. Whether youre editing videos, rendering 3D graphics, or streaming gameplay, this processor provides the power you need to stay productive.</p>
                <h2>Unleash Gaming Potential</h2>
                <p>Equipped with Intel Turbo Boost Max Technology 3.0, the Core i9-13900KF delivers incredible gaming performance, ensuring smooth frame rates and responsive gameplay even in the most demanding titles. Experience gaming like never before with this powerhouse CPU.</p>
                <h2>Next-Gen Connectivity</h2>
                <p>Featuring PCIe Gen 5 and DDR5 memory support, the Core i9-13900KF offers lightning-fast data transfer speeds and improved system responsiveness. Connect high-speed peripherals, upgrade to the latest memory technology, and take your computing experience to new heights.</p>
                <h2>Efficient Power Management</h2>
                <p>With Intels Enhanced SpeedStep and Deep Sleep technologies, the Core i9-13900KF optimizes power efficiency without compromising performance. Enjoy longer battery life on laptops and reduced power consumption on desktops, ensuring a more energy-efficient computing experience.</p>
                <h2>Unrivaled Productivity</h2>
                <p>Whether youre gaming, creating content, or tackling everyday tasks, the Intel Core i9-13900KF empowers you to unleash your creativity and accomplish more. From gaming to content creation and everything in between, this powerful CPU enables you to do it all with unmatched speed and efficiency.</p>""",
            "sale_id": None,
        },
        {
            "id": 103,
            "name": "Intel Core i7-13700",
            "price": 500.0,
            "old_price": 600.0,
            "description": """<h2>Unleash Your Potential</h2>
                <p>Introducing the Intel Core i7-13700, a high-performance processor designed to elevate your computing experience to new heights. Built on Intels cutting-edge 12th generation Alder Lake architecture, this CPU delivers exceptional performance for both productivity and gaming tasks.</p>
                <h2>Powerful Multitasking</h2>
                <p>With 8 cores and 16 threads, the Core i7-13700 offers powerful multitasking capabilities, allowing you to tackle demanding workloads with ease. Whether youre running multiple applications simultaneously or streaming content while gaming, this processor delivers smooth and responsive performance.</p>
                <h2>Enhanced Gaming Experience</h2>
                <p>Equipped with Intel Turbo Boost Max Technology 3.0, the Core i7-13700 ensures a seamless gaming experience with high frame rates and low latency. Enjoy immersive gaming sessions with stunning visuals and responsive gameplay, thanks to the power of this CPU.</p>
                <h2>Next-Gen Connectivity</h2>
                <p>Featuring support for PCIe Gen 5 and DDR5 memory, the Core i7-13700 offers lightning-fast data transfer speeds and improved system responsiveness. Connect high-speed storage devices, upgrade to the latest memory technology, and experience faster load times and smoother performance.</p>
                <h2>Efficient Power Management</h2>
                <p>With Intels Enhanced SpeedStep and Deep Sleep technologies, the Core i7-13700 optimizes power efficiency without sacrificing performance. Enjoy longer battery life on laptops and reduced power consumption on desktops, ensuring a more energy-efficient computing experience.</p>
                <h2>Unrivaled Performance</h2>
                <p>Whether youre gaming, streaming, or creating content, the Intel Core i7-13700 empowers you to unleash your creativity and accomplish more. With its powerful combination of performance and efficiency, this CPU delivers the speed and responsiveness you need to excel in any task.</p>""",
            "sale_id": None,
        },
        {
            "id": 104,
            "name": "Intel Core i9-13900K",
            "price": 550.0,
            "old_price": 580.0,
            "description": """<h2>Unleash Unprecedented Power</h2>
                <p>Introducing the Intel Core i9-13900K, the pinnacle of performance in Intels 12th generation Alder Lake lineup. Designed for enthusiasts and power users, this CPU delivers unparalleled power and speed to handle the most demanding tasks with ease.</p>
                <h2>Unmatched Processing Power</h2>
                <p>With 16 cores and 24 threads, the Core i9-13900K redefines whats possible in computing. Experience lightning-fast performance and seamless multitasking, whether youre gaming, streaming, or creating content. Take your productivity to new heights and accomplish more in less time.</p>
                <h2>Boosted Gaming Performance</h2>
                <p>Equipped with Intel Turbo Boost Max Technology 3.0, the Core i9-13900K unleashes maximum gaming performance when you need it most. Enjoy smooth gameplay, high frame rates, and immersive visuals, even in the most demanding AAA titles.</p>
                <h2>Next-Generation Connectivity</h2>
                <p>With support for PCIe Gen 5 and DDR5 memory, the Core i9-13900K offers blazing-fast data transfer speeds and ultra-low latency. Connect high-speed storage devices, upgrade to the latest memory technology, and experience unparalleled responsiveness in every application.</p>
                <h2>Efficient Thermal Design</h2>
                <p>Featuring Intels advanced thermal design, the Core i9-13900K ensures optimal heat dissipation and temperature management under heavy workloads. Keep your system cool and stable, even during extended gaming sessions or intense content creation tasks.</p>
                <h2>Unleash Your Creativity</h2>
                <p>Whether youre editing videos, rendering 3D models, or compiling code, the Core i9-13900K empowers you to unleash your creativity without compromise. Experience unparalleled performance and responsiveness, and take your work to the next level.</p>
                <h2>Unlock Your Potential</h2>
                <p>With the Intel Core i9-13900K, the possibilities are limitless. Push the boundaries of performance, unleash your creativity, and unlock new opportunities in gaming, content creation, and beyond. Experience the ultimate in desktop computing power with the Core i9-13900K.</p>""",
            "sale_id": None,
        },
        {
            "id": 105,
            "name": "Intel Core i3-13100",
            "price": 200.0,
            "old_price": 300.0,
            "description": """<h2>Next-Level Performance</h2>
                <p>Meet the Intel Core i3-13100, a powerhouse processor designed to elevate your computing experience to the next level. With impressive performance and advanced features, this CPU is perfect for productivity, gaming, and everyday tasks.</p>
                <h2>Smooth Multitasking</h2>
                <p>Equipped with 4 cores and 8 threads, the Core i3-13100 delivers smooth multitasking performance, allowing you to breeze through everyday tasks with ease. Whether youre browsing the web, streaming content, or working on office applications, this processor ensures responsive performance.</p>
                <h2>Enhanced Gaming Experience</h2>
                <p>Experience immersive gaming like never before with the Intel Core i3-13100. With support for Intel Hyper-Threading Technology, this processor delivers improved gaming performance, allowing you to enjoy smoother gameplay and faster frame rates in your favorite titles.</p>
                <h2>Efficient Power Consumption</h2>
                <p>Thanks to Intels advanced manufacturing process, the Core i3-13100 delivers impressive performance while maintaining efficient power consumption. Enjoy long battery life on laptops or lower energy bills on desktops, without compromising on performance.</p>
                <h2>Integrated Graphics</h2>
                <p>The Core i3-13100 features integrated Intel UHD Graphics, providing crisp visuals and smooth video playback for multimedia tasks. Whether youre watching movies, editing photos, or browsing the web, this processor delivers stunning visuals with ease.</p>
                <h2>Advanced Connectivity</h2>
                <p>With support for the latest connectivity standards, including PCIe Gen 4 and DDR5 memory, the Core i3-13100 ensures blazing-fast data transfer speeds and ultra-low latency. Connect high-speed storage devices, upgrade to the latest memory technology, and experience responsive performance in every application.</p>
                <h2>Upgrade Your Experience</h2>
                <p>Upgrade to the Intel Core i3-13100 and experience a new level of performance, efficiency, and responsiveness. Whether youre a casual user, a content creator, or a gamer, this processor delivers the performance you need to tackle any task with confidence.</p>""",
            "sale_id": None,
        },
        {
            "id": 106,
            "name": "Logitech MX Master 3S Grafit",
            "price": 99.99,
            "old_price": 129.99,
            "description": """<h2>Precision and Comfort</h2>
                <p>Experience unparalleled precision with the Logitech MX Master 3S Grafit. Designed for professionals and enthusiasts alike, this mouse offers seamless control and exceptional comfort for extended use.</p>
                <h2>Advanced Tracking</h2>
                <p>The MX Master 3S features Logitech's advanced Darkfield High Precision sensor, enabling accurate tracking on virtually any surface, including glass. Enjoy smooth and responsive cursor movements whether you're working on a desk or a glass table.</p>
                <h2>Customizable Buttons</h2>
                <p>With multiple customizable buttons, the MX Master 3S allows you to tailor your workflow to your specific needs. Assign shortcuts, macros, and commands to enhance productivity and streamline your tasks.</p>
                <h2>Ergonomic Design</h2>
                <p>Designed with ergonomics in mind, the MX Master 3S provides a comfortable grip and optimal hand positioning. Its sculpted shape reduces strain and fatigue, making it ideal for long hours of use.</p>
                <h2>Seamless Connectivity</h2>
                <p>Connect effortlessly via Bluetooth or the included USB receiver. The MX Master 3S supports easy switching between multiple devices, allowing you to manage your workflow across different systems with ease.</p>
                <h2>Long-Lasting Battery</h2>
                <p>Enjoy up to 70 days of battery life on a single charge. The fast-charging feature ensures that you spend less time charging and more time being productive.</p>
                <h2>Elegant Aesthetics</h2>
                <p>The Grafit color variant offers a sleek and professional look that complements any workspace. Its minimalist design blends seamlessly with your office environment.</p>""",
            "sale_id": None,
        },
        {
            "id": 107,
            "name": "Logitech M705 Marathon",
            "price": 49.99,
            "old_price": 59.99,
            "description": """<h2>Endurance for Long Sessions</h2>
                <p>The Logitech M705 Marathon is built to last with an impressive battery life that can go up to 3 years on a single set of batteries. Perfect for users who need a reliable mouse without the hassle of frequent replacements.</p>
                <h2>Comfortable Grip</h2>
                <p>Designed for extended use, the M705 Marathon offers a comfortable ergonomic design that fits naturally in your hand, reducing fatigue during long work or gaming sessions.</p>
                <h2>High Precision Tracking</h2>
                <p>Equipped with Logitech's optical sensor, the M705 ensures precise tracking and smooth cursor movement on a variety of surfaces, enhancing your overall user experience.</p>
                <h2>Customizable Buttons</h2>
                <p>With six customizable buttons, the Marathon allows you to assign your favorite shortcuts and macros, making navigation and task management more efficient.</p>
                <h2>Smart Scroll Wheel</h2>
                <p>The hyper-fast scroll wheel can switch between ratchet and free-spin modes, allowing you to scroll through documents and webpages with ease and speed.</p>
                <h2>Multi-Device Connectivity</h2>
                <p>Connect the M705 Marathon to up to three devices simultaneously and switch between them seamlessly with the touch of a button, perfect for multitasking across different platforms.</p>
                <h2>Reliable Wireless Performance</h2>
                <p>The Marathon uses a reliable 2.4 GHz wireless connection, ensuring stable and uninterrupted performance for all your computing needs.</p>""",
            "sale_id": None,
        },
        {
            "id": 108,
            "name": "SteelSeries Rival 650",
            "price": 89.99,
            "old_price": 109.99,
            "description": """<h2>Dual Motor Vibration Feedback</h2>
                <p>The SteelSeries Rival 650 offers immersive dual motor vibration feedback, delivering precise and realistic haptic responses for a more engaging gaming experience.</p>
                <h2>TrueMove3+ Optical Sensor</h2>
                <p>Equipped with the TrueMove3+ sensor, the Rival 650 provides true 1-to-1 tracking with zero acceleration, ensuring pinpoint accuracy in every movement.</p>
                <h2>Customizable Weight System</h2>
                <p>Adjust the mouse's weight with the customizable weight system, allowing you to fine-tune the feel and balance to match your personal preferences.</p>
                <h2>Detachable Cable</h2>
                <p>The Rival 650 features a detachable braided cable, providing durability and the flexibility to switch between wired and wireless play seamlessly.</p>
                <h2>RGB Lighting</h2>
                <p>Personalize your Rival 650 with customizable RGB lighting, enabling you to match your setup's aesthetic or highlight key actions during gameplay.</p>
                <h2>Comfortable Ergonomic Design</h2>
                <p>Designed for long gaming sessions, the Rival 650 offers a comfortable ergonomic shape that supports your hand and reduces fatigue.</p>
                <h2>Advanced Software Integration</h2>
                <p>Use the SteelSeries Engine software to customize settings, assign macros, and create profiles tailored to different games or applications.</p>""",
            "sale_id": None,
        },
        {
            "id": 109,
            "name": "Logitech G502 HERO",
            "price": 79.99,
            "old_price": 99.99,
            "description": """<h2>Unmatched Precision with HERO Sensor</h2>
                <p>The Logitech G502 HERO features the HERO 25K sensor, delivering exceptional precision and performance with up to 25,600 DPI, ensuring every movement is captured accurately.</p>
                <h2>Customizable Buttons</h2>
                <p>With 11 programmable buttons, the G502 HERO allows you to assign complex macros and shortcuts, giving you a competitive edge in your favorite games.</p>
                <h2>Adjustable Weight System</h2>
                <p>Customize the mouse's weight and balance with up to 5 removable weights, allowing you to fine-tune the feel to suit your gaming style.</p>
                <h2>Advanced Onboard Memory</h2>
                <p>Save your profiles directly to the mouse's onboard memory, enabling you to carry your settings wherever you go without needing to reconfigure.</p>
                <h2>RGB Lighting</h2>
                <p>Illuminate your setup with customizable RGB lighting, enhancing both aesthetics and visibility during intense gaming sessions.</p>
                <h2>Durable Construction</h2>
                <p>Built to withstand the rigors of competitive gaming, the G502 HERO features high-quality materials and durable switches rated for millions of clicks.</p>
                <h2>Comfortable Ergonomic Design</h2>
                <p>Designed for extended gaming sessions, the ergonomic shape of the G502 HERO provides a comfortable grip and reduces hand fatigue.</p>""",
            "sale_id": None,
        },
        {
            "id": 110,
            "name": "Razer Basilisk V3",
            "price": 69.99,
            "old_price": 89.99,
            "description": """<h2>Precision at Your Fingertips</h2>
                <p>The Razer Basilisk V3 is engineered for gamers who demand precision and performance. Featuring a high-accuracy sensor and customizable settings, this mouse ensures you stay ahead in every game.</p>
                <h2>Customizable Scroll Wheel Tension</h2>
                <p>Adjust the scroll wheel tension to your liking, allowing for precise control whether you're navigating menus or executing rapid-fire commands.</p>
                <h2>Ergonomic Design with Customizable Features</h2>
                <p>Designed for comfort, the Basilisk V3 offers an ergonomic shape that fits naturally in your hand. Customize the side grips, DPI settings, and button assignments to match your gaming style.</p>
                <h2>Razer Chroma RGB Lighting</h2>
                <p>Enhance your gaming setup with vibrant Razer Chroma RGB lighting. Sync the lighting effects with your gameplay for an immersive experience.</p>
                <h2>Programmable Buttons</h2>
                <p>With multiple programmable buttons, the Basilisk V3 allows you to assign complex macros and shortcuts, giving you quick access to your most-used commands.</p>
                <h2>Durable Build Quality</h2>
                <p>Built to last, the Basilisk V3 features durable switches and high-quality materials that withstand intense gaming sessions and continuous use.</p>
                <h2>Seamless Integration with Razer Synapse</h2>
                <p>Customize your mouse settings effortlessly with Razer Synapse software. Save profiles, adjust DPI settings, and fine-tune your lighting preferences with ease.</p>""",
            "sale_id": None,
        },
        {
            "id": 111,
            "name": "Silver Monkey X Howler",
            "price": 59.99,
            "old_price": 79.99,
            "description": """<h2>Unmatched Durability</h2>
                <p>The Silver Monkey X Howler is built to endure even the most intense gaming sessions. Featuring reinforced materials and high-quality construction, this mouse is designed to last.</p>
                <h2>High-Precision Sensor</h2>
                <p>Equipped with a high-precision optical sensor, the Howler offers accurate tracking and responsive performance, ensuring every move you make is executed flawlessly.</p>
                <h2>Customizable Buttons</h2>
                <p>With multiple programmable buttons, the Howler allows you to assign macros and shortcuts, enhancing your gaming efficiency and providing quick access to essential commands.</p>
                <h2>Ergonomic Comfort</h2>
                <p>Designed for comfort, the Howler features an ergonomic shape that fits naturally in your hand, reducing fatigue during extended gaming sessions.</p>
                <h2>Adjustable DPI Settings</h2>
                <p>Switch between various DPI settings on-the-fly to match your gaming needs, whether you're sniping from a distance or engaging in close-quarters combat.</p>
                <h2>RGB Lighting</h2>
                <p>Personalize your mouse with customizable RGB lighting, adding a touch of style to your gaming setup and enhancing visual appeal.</p>
                <h2>Seamless Software Integration</h2>
                <p>Use the accompanying software to customize your mouse settings, save profiles, and synchronize lighting effects with your other gaming peripherals.</p>""",
            "sale_id": None,
        },
        {
            "id": 112,
            "name": "Logitech M185 Szara",
            "price": 19.99,
            "old_price": 24.99,
            "description": """<h2>Compact and Reliable</h2>
                <p>The Logitech M185 Szara is a compact and reliable wireless mouse, perfect for everyday use in both home and office environments. Its sleek design and dependable performance make it a great addition to any setup.</p>
                <h2>Plug-and-Play Connectivity</h2>
                <p>Connect the M185 effortlessly using the included USB receiver. No drivers are required, allowing you to start using the mouse immediately after plugging it in.</p>
                <h2>Comfortable Grip</h2>
                <p>Designed for comfort, the M185 Szara offers a smooth and responsive glide, making navigation across various surfaces effortless and comfortable.</p>
                <h2>Long Battery Life</h2>
                <p>Enjoy extended use with the M185's long battery life. Its power-efficient design ensures that you can rely on the mouse for days without needing to replace the batteries.</p>
                <h2>Quiet Clicks</h2>
                <p>The M185 features quiet clicking, providing a discreet and pleasant user experience, ideal for office settings and shared workspaces.</p>
                <h2>Durable Build</h2>
                <p>Constructed with high-quality materials, the Logitech M185 Szara is built to withstand daily use, ensuring longevity and sustained performance.</p>
                <h2>Simple and Elegant Design</h2>
                <p>With its minimalist design and neutral gray color, the M185 Szara complements any workspace, adding a touch of elegance without compromising functionality.</p>""",
            "sale_id": None,
        },
        {
            "id": 113,
            "name": "SteelSeries Rival 3",
            "price": 39.99,
            "old_price": 49.99,
            "description": """<h2>High-Performance Gaming</h2>
                <p>The SteelSeries Rival 3 is a budget-friendly gaming mouse that doesn't compromise on performance. Featuring a high-precision sensor and durable build, it's perfect for gamers looking for quality without breaking the bank.</p>
                <h2>TrueMove Core Sensor</h2>
                <p>Equipped with the TrueMove Core optical sensor, the Rival 3 delivers true 1-to-1 tracking with up to 8,500 CPI, ensuring accurate and responsive movements in every game.</p>
                <h2>Durable Construction</h2>
                <p>Designed to withstand intense gaming sessions, the Rival 3 features SteelSeries' legendary durability with PTFE feet and high-grade materials that ensure longevity.</p>
                <h2>Customizable RGB Lighting</h2>
                <p>Enhance your gaming setup with customizable RGB lighting. Choose from multiple color options to match your style or highlight your in-game actions.</p>
                <h2>Six Programmable Buttons</h2>
                <p>With six programmable buttons, the Rival 3 allows you to assign macros and shortcuts, giving you quick access to essential commands and improving your gameplay efficiency.</p>
                <h2>Comfortable Ergonomic Design</h2>
                <p>The Rival 3 is designed for comfort, featuring an ergonomic shape that fits naturally in your hand, reducing fatigue during long gaming sessions.</p>
                <h2>SteelSeries Engine Integration</h2>
                <p>Customize your mouse settings effortlessly with SteelSeries Engine software. Create profiles, adjust DPI settings, and synchronize lighting effects to enhance your gaming experience.</p>""",
            "sale_id": None,
        },
        {
            "id": 114,
            "name": "SteelSeries Rival 5",
            "price": 59.99,
            "old_price": 74.99,
            "description": """<h2>Ultimate Gaming Precision</h2>
                <p>The SteelSeries Rival 5 takes gaming precision to the next level with its advanced sensor technology and customizable features. Designed for competitive gamers, this mouse ensures every move is executed with utmost accuracy.</p>
                <h2>TrueMove Pro+ Sensor</h2>
                <p>Equipped with the TrueMove Pro+ optical sensor, the Rival 5 offers true 1-to-1 tracking with up to 16,000 CPI, providing unmatched accuracy and responsiveness in every game.</p>
                <h2>Customizable Weight System</h2>
                <p>Tailor the mouse's weight and balance with the customizable weight system, allowing you to fine-tune the feel to match your personal gaming style and preferences.</p>
                <h2>RGB Lighting and Customization</h2>
                <p>Personalize your Rival 5 with customizable RGB lighting. Sync the lighting effects with your other SteelSeries devices for a cohesive and immersive gaming setup.</p>
                <h2>Programmable Buttons</h2>
                <p>With eight programmable buttons, the Rival 5 provides extensive customization options. Assign macros, shortcuts, and commands to enhance your gameplay and improve your efficiency.</p>
                <h2>Durable and Ergonomic Design</h2>
                <p>Built to last, the Rival 5 features high-quality materials and a comfortable ergonomic design that supports your hand during long gaming sessions, reducing fatigue and enhancing performance.</p>
                <h2>SteelSeries Engine Integration</h2>
                <p>Use the SteelSeries Engine software to customize your mouse settings, create profiles, and synchronize lighting effects, ensuring your Rival 5 is always optimized for your gaming needs.</p>""",
            "sale_id": None,
        },
        {
            "id": 115,
            "name": "Razer Basilisk V3 X HyperSpeed",
            "price": 89.99,
            "old_price": 109.99,
            "description": """<h2>Revolutionary Wireless Performance</h2>
                <p>The Razer Basilisk V3 X HyperSpeed combines the best of wired precision and wireless freedom. Featuring Razer's HyperSpeed wireless technology, this mouse delivers lag-free performance with ultra-low latency.</p>
                <h2>Advanced Sensor Technology</h2>
                <p>Equipped with a high-precision optical sensor, the Basilisk V3 X HyperSpeed offers up to 20,000 DPI, ensuring accurate tracking and responsive performance in every game.</p>
                <h2>Customizable Ergonomic Design</h2>
                <p>Designed for comfort, the Basilisk V3 X HyperSpeed features an ergonomic shape with customizable side grips and adjustable features to suit your hand size and gaming style.</p>
                <h2>Programmable Buttons and RGB Lighting</h2>
                <p>With multiple programmable buttons and customizable RGB lighting, the Basilisk V3 X HyperSpeed allows you to personalize your mouse to match your setup and optimize your gameplay.</p>
                <h2>HyperSpeed Wireless Technology</h2>
                <p>Experience the freedom of wireless gaming without compromising on performance. Razer's HyperSpeed technology ensures a stable and fast connection, giving you a competitive edge.</p>
                <h2>Long Battery Life</h2>
                <p>Enjoy extended gaming sessions with the Basilisk V3 X HyperSpeed's long-lasting battery. Charge quickly and get back to your game in no time.</p>
                <h2>Durable Build and Premium Materials</h2>
                <p>The Basilisk V3 X HyperSpeed is built with high-quality materials, ensuring durability and longevity even during the most intense gaming sessions.</p>""",
            "sale_id": None,
        },
        {
            "id": 116,
            "name": "RAPOO ZESTAW BEZPRZEWODOWY MULTI-MODE 9310M CZARNY",
            "price": 59.99,
            "old_price": 79.99,
            "description": """<h2>Wireless Convenience</h2>
                <p>The RAPOO Zestaw Bezprzewodowy Multi-Mode 9310M Czarny offers seamless wireless connectivity, allowing you to switch effortlessly between multiple devices with its multi-mode functionality.</p>
                <h2>Ergonomic Design</h2>
                <p>Designed for comfort, this keyboard provides a sleek and ergonomic layout that reduces strain during extended typing sessions.</p>
                <h2>Reliable Performance</h2>
                <p>Equipped with a responsive keyboard switch, the 9310M ensures accurate and swift keystrokes for both work and play.</p>
                <h2>Long Battery Life</h2>
                <p>Enjoy uninterrupted use with the extended battery life, perfect for long hours without the need for frequent recharging.</p>
                <h2>Compact and Stylish</h2>
                <p>The compact black design not only saves desk space but also complements any workspace aesthetic.</p>""",
            "sale_id": None,
        },
        {
            "id": 117,
            "name": "Dark Project ALU87A Onionite Wired G3MS Amber",
            "price": 89.99,
            "old_price": 119.99,
            "description": """<h2>High-Performance Wired Connection</h2>
                <p>The Dark Project ALU87A Onionite Wired G3MS Amber ensures a stable and fast connection, eliminating lag for an enhanced gaming and typing experience.</p>
                <h2>Mechanical Switches</h2>
                <p>Featuring durable mechanical switches, this keyboard provides tactile feedback and longevity, perfect for both gamers and professionals.</p>
                <h2>Customizable RGB Lighting</h2>
                <p>Personalize your setup with vibrant amber RGB lighting, allowing you to create the perfect ambiance for any environment.</p>
                <h2>Anti-Ghosting Keys</h2>
                <p>With full N-Key rollover, the ALU87A ensures that every keypress is registered accurately, even during intense gaming sessions.</p>
                <h2>Ergonomic Layout</h2>
                <p>The ergonomic design with a detachable wrist rest offers comfort and support, reducing fatigue during prolonged use.</p>""",
            "sale_id": None,
        },
        {
            "id": 118,
            "name": "Dark Project DPO87 Black TKL G3MS Sapphire Hot-Swap",
            "price": 109.99,
            "old_price": 149.99,
            "description": """<h2>Tenkeyless Design</h2>
                <p>The Dark Project DPO87 Black TKL G3MS Sapphire Hot-Swap offers a compact tenkeyless layout, saving desk space while maintaining essential functionality for both gaming and productivity.</p>
                <h2>Hot-Swap Capability</h2>
                <p>Easily customize your typing experience with hot-swap switches, allowing you to change switches without soldering.</p>
                <h2>Sapphire RGB Lighting</h2>
                <p>Enhance your setup with stunning sapphire RGB lighting, providing dynamic lighting effects that can be customized to your preference.</p>
                <h2>Durable Construction</h2>
                <p>Built with high-quality materials, the DPO87 ensures durability and longevity, even under heavy use.</p>
                <h2>Advanced Key Rollover</h2>
                <p>Experience precise and simultaneous key presses with advanced key rollover technology, ensuring every input is registered accurately.</p>""",
            "sale_id": None,
        },
        {
            "id": 119,
            "name": "Silver Monkey X Mandrill",
            "price": 129.99,
            "old_price": 159.99,
            "description": """<h2>Premium Wireless Performance</h2>
                <p>The Silver Monkey X Mandrill offers top-tier wireless connectivity with minimal latency, perfect for both gaming and professional use.</p>
                <h2>Mechanical Key Switches</h2>
                <p>Equipped with high-quality mechanical switches, the Mandrill provides tactile feedback and exceptional durability for a superior typing experience.</p>
                <h2>Customizable Lighting</h2>
                <p>Illuminate your workspace with customizable RGB lighting, allowing you to personalize the keyboard to match your style.</p>
                <h2>Ergonomic Design</h2>
                <p>Designed for comfort, the Mandrill features an ergonomic layout with a detachable wrist rest, reducing strain during extended use.</p>
                <h2>Programmable Macros</h2>
                <p>Enhance your productivity and gaming performance with programmable macros, giving you quick access to your most-used commands.</p>""",
            "sale_id": None,
        },
        {
            "id": 120,
            "name": "Keychron K5SE Slim Low Profile Red Switch HS RGB Full Size ALU",
            "price": 139.99,
            "old_price": 169.99,
            "description": """<h2>Slim Low Profile Design</h2>
                <p>The Keychron K5SE Slim Low Profile Red Switch HS RGB Full Size ALU combines a sleek, low-profile design with full-size functionality, perfect for modern workspaces.</p>
                <h2>Red Mechanical Switches</h2>
                <p>Experience smooth and silent typing with Red mechanical switches, ideal for both gaming and office environments.</p>
                <h2>RGB Backlighting</h2>
                <p>Customize your keyboard with vibrant RGB backlighting, featuring multiple lighting effects to suit your preference.</p>
                <h2>Full-Size Layout</h2>
                <p>Enjoy all the keys you need with a full-size layout, including a numeric keypad, without compromising on slim aesthetics.</p>
                <h2>Wireless and Wired Modes</h2>
                <p>Switch effortlessly between wireless Bluetooth connectivity and a wired USB-C connection, offering flexibility for any setup.</p>""",
            "sale_id": None,
        },
        {
            "id": 121,
            "name": "Dark Project DPO87 Violet Horizon Combo G3MS Sapphire",
            "price": 149.99,
            "old_price": 189.99,
            "description": """<h2>Comprehensive Gaming Combo</h2>
                <p>The Dark Project DPO87 Violet Horizon Combo G3MS Sapphire includes both a high-performance keyboard and mouse, providing a complete setup for an immersive gaming experience.</p>
                <h2>Violet Horizon RGB Lighting</h2>
                <p>Customize your gaming environment with stunning violet RGB lighting, synchronized across both the keyboard and mouse for a cohesive look.</p>
                <h2>Mechanical Key Switches</h2>
                <p>Enjoy responsive and durable mechanical key switches on the DPO87 keyboard, ensuring precise and tactile feedback for every keystroke.</p>
                <h2>High-Precision Mouse</h2>
                <p>The included G3MS Sapphire mouse features a high-precision sensor and customizable buttons, enhancing your control and responsiveness in games.</p>
                <h2>Durable Build Quality</h2>
                <p>Both the keyboard and mouse are built with premium materials, ensuring longevity and reliability during intense gaming sessions.</p>""",
            "sale_id": None,
        },
        {
            "id": 122,
            "name": "Dell Pro Keyboard and Mouse KM5221W",
            "price": 69.99,
            "old_price": 89.99,
            "description": """<h2>Professional Workstation Setup</h2>
                <p>The Dell Pro Keyboard and Mouse KM5221W offers a reliable and efficient setup for professional environments, ensuring productivity and comfort.</p>
                <h2>Quiet and Responsive Typing</h2>
                <p>The keyboard features quiet keys that provide responsive and comfortable typing, perfect for office settings where noise reduction is essential.</h2>
                <h2>Ergonomic Mouse Design</h2>
                <p>The mouse is ergonomically designed to fit comfortably in your hand, reducing strain during long hours of use.</p>
                <h2>Wireless Connectivity</h2>
                <p>Enjoy a clutter-free workspace with wireless connectivity, easily connecting via Bluetooth or the included USB receiver.</p>
                <h2>Durable and Long-Lasting</h2>
                <p>Built with durability in mind, both the keyboard and mouse are constructed to withstand daily use, ensuring longevity and consistent performance.</p>""",
            "sale_id": None,
        },
        {
            "id": 123,
            "name": "Silver Monkey K90 Wireless Premium Business Keyboard (Grey)",
            "price": 119.99,
            "old_price": 149.99,
            "description": """<h2>Premium Wireless Connectivity</h2>
                <p>The Silver Monkey K90 Wireless Premium Business Keyboard in Grey offers seamless wireless connectivity, providing flexibility and a clean workspace for business professionals.</p>
                <h2>Mechanical Blue Switches</h2>
                <p>Experience tactile and audible feedback with mechanical blue switches, ensuring precise and satisfying keystrokes for efficient typing.</h2>
                <h2>RGB Backlighting</h2>
                <p>Enhance your workspace with customizable RGB backlighting, allowing you to adjust the lighting to match your preferences and environment.</p>
                <h2>Full-Size Layout</h2>
                <p>The full-size layout includes a numeric keypad, providing all the keys you need for comprehensive business tasks without compromising on style.</p>
                <h2>Durable Aluminum Build</h2>
                <p>Constructed with a premium aluminum frame, the K90 ensures durability and a sleek, professional appearance suitable for any office setting.</p>""",
            "sale_id": None,
        },
        {
            "id": 124,
            "name": "Dell KB216-B QuietKey USB (Czarna)",
            "price": 29.99,
            "old_price": 39.99,
            "description": """<h2>QuietKey Technology</h2>
                <p>The Dell KB216-B QuietKey USB keyboard features Dell's QuietKey technology, providing a silent and comfortable typing experience ideal for shared workspaces.</p>
                <h2>Plug-and-Play USB Connection</h2>
                <p>Simply connect the keyboard via USB and start typing immediately without the need for additional drivers or software.</p>
                <h2>Compact and Sleek Design</h2>
                <p>With its compact and sleek black design, the KB216-B fits seamlessly into any workspace, offering both style and functionality.</p>
                <h2>Durable Build</h2>
                <p>Built to last, this keyboard is constructed with high-quality materials that ensure durability and long-term reliability.</p>
                <h2>Full-Size Layout</h2>
                <p>The full-size layout includes all essential keys, including a numeric keypad, making it suitable for various business and personal tasks.</p>""",
            "sale_id": None,
        },
        {
            "id": 125,
            "name": "SteelSeries Apex 7 Blue Switch",
            "price": 149.99,
            "old_price": 179.99,
            "description": """<h2>OmniPoint Adjustable Mechanical Switches</h2>
                <p>The SteelSeries Apex 7 Blue Switch keyboard features OmniPoint switches that allow you to adjust the actuation point, providing customizable typing and gaming experiences.</p>
                <h2>RGB Illumination</h2>
                <p>Enhance your setup with vibrant RGB illumination, offering dynamic lighting effects that can be customized to match your style and preferences.</h2>
                <h2>Dedicated Multimedia Controls</h2>
                <p>Conveniently control your media with dedicated multimedia keys, allowing easy access to volume, playback, and more without interrupting your workflow.</p>
                <h2>Durable Aluminum Frame</h2>
                <p>Constructed with a premium aluminum frame, the Apex 7 ensures durability and a sleek, professional appearance suitable for any environment.</p>
                <h2>N-Key Rollover and Anti-Ghosting</h2>
                <p>Experience flawless performance with N-key rollover and anti-ghosting technology, ensuring every keypress is registered accurately, even during intense gaming sessions.</p>""",
            "sale_id": None,
        },
        {
            "id": 126,
            "name": "Samsung Odyssey G5 S27DG500EUX G50D",
            "price": 399.99,
            "old_price": 499.99,
            "description": """<h2>Immersive Curved Display</h2>
                <p>The Samsung Odyssey G5 S27DG500EUX G50D features a 27-inch curved VA panel with a 1000R curvature, providing an immersive viewing experience that wraps around your field of vision for enhanced depth and realism.</p>
                <h2>High Refresh Rate</h2>
                <p>Enjoy smooth and fluid visuals with a 165Hz refresh rate, reducing motion blur and ensuring a competitive edge in fast-paced gaming scenarios.</p>
                <h2>Rapid Response Time</h2>
                <p>Equipped with a 1ms MPRT response time, the Odyssey G5 minimizes ghosting and blurring, delivering crisp and clear images even during intense action sequences.</p>
                <h2>Adaptive Sync Technology</h2>
                <p>Experience tear-free gaming with AMD FreeSync Premium support, synchronizing the monitor's refresh rate with your GPU to eliminate screen tearing and stuttering.</p>
                <h2>Vivid Color Reproduction</h2>
                <p>The monitor boasts a 1440p resolution and a 178° viewing angle, ensuring vibrant and accurate colors from any perspective, making it ideal for both gaming and professional use.</p>""",
            "sale_id": None,
        },
        {
            "id": 127,
            "name": "LG UltraGear 27GS60QC-B",
            "price": 349.99,
            "old_price": 429.99,
            "description": """<h2>Stunning 27-Inch Display</h2>
                <p>The LG UltraGear 27GS60QC-B offers a 27-inch QHD display with a 144Hz refresh rate, delivering sharp and detailed visuals that enhance your gaming and productivity tasks.</p>
                <h2>Adaptive Sync Compatibility</h2>
                <p>With support for both AMD FreeSync and NVIDIA G-SYNC Compatible, this monitor ensures smooth and tear-free gameplay by synchronizing the display's refresh rate with your graphics card.</p>
                <h2>Ultra-Thin Bezel Design</h2>
                <p>The sleek ultra-thin bezel minimizes distractions and provides a seamless multi-monitor setup, allowing you to expand your workspace effortlessly.</p>
                <h2>Advanced Gaming Features</h2>
                <p>Features like Dynamic Action Sync and Black Stabilizer enhance your gaming performance by reducing input lag and improving visibility in dark scenes.</p>
                <h2>Ergonomic Stand</h2>
                <p>The adjustable stand allows you to tilt, swivel, and adjust the height of the monitor to achieve the perfect viewing angle, ensuring maximum comfort during extended use.</p>""",
            "sale_id": None,
        },
        {
            "id": 128,
            "name": "MSI G27CQ4 E2",
            "price": 379.99,
            "old_price": 459.99,
            "description": """<h2>Curved QHD Display</h2>
                <p>The MSI G27CQ4 E2 features a 27-inch curved QHD display with a 165Hz refresh rate, providing an immersive and responsive gaming experience that brings your games to life.</p>
                <h2>Fast Response Time</h2>
                <p>With a 1ms MPRT response time, this monitor ensures minimal motion blur and ghosting, allowing for sharp and clear visuals during high-speed action.</p>
                <h2>Adaptive Sync Technology</h2>
                <p>Equipped with AMD FreeSync Premium, the G27CQ4 E2 eliminates screen tearing and stuttering by synchronizing the monitor's refresh rate with your GPU.</p>
                <h2>Vibrant Color Accuracy</h2>
                <p>Boasting a VA panel with 100% sRGB coverage, the monitor delivers rich and accurate colors, enhancing both gaming and content creation.</p>
                <h2>Ergonomic and Stylish Design</h2>
                <p>The sleek design with an adjustable stand allows for comfortable viewing angles, while customizable RGB lighting adds a touch of style to your gaming setup.</p>""",
            "sale_id": None,
        },
        {
            "id": 129,
            "name": "Dell G2724D",
            "price": 329.99,
            "old_price": 399.99,
            "description": """<h2>27-Inch QHD Display</h2>
                <p>The Dell G2724D offers a 27-inch QHD (2560x1440) display, delivering sharp and detailed visuals that enhance your gaming and multimedia experiences.</p>
                <h2>High Refresh Rate</h2>
                <p>With a 165Hz refresh rate, this monitor ensures ultra-smooth gameplay, allowing you to react faster and gain a competitive edge in fast-paced games.</p>
                <h2>AMD FreeSync Premium</h2>
                <p>Experience tear-free and stutter-free gaming with AMD FreeSync Premium, which synchronizes the monitor's refresh rate with your GPU for seamless visuals.</p>
                <h2>Low Input Lag</h2>
                <p>Designed for gamers, the G2724D features low input lag and a fast response time of 1ms MPRT, ensuring your actions are displayed instantaneously on the screen.</p>
                <h2>Ergonomic Adjustments</h2>
                <p>The adjustable stand allows you to tilt, swivel, and adjust the height of the monitor, providing a comfortable viewing angle for extended gaming sessions.</p>""",
            "sale_id": None,
        },
        {
            "id": 130,
            "name": "MSI G24C4 E2",
            "price": 249.99,
            "old_price": 299.99,
            "description": """<h2>24-Inch Curved Display</h2>
                <p>The MSI G24C4 E2 features a 24-inch curved VA panel with a 144Hz refresh rate, offering an immersive and smooth visual experience for both gaming and everyday use.</p>
                <h2>Rapid Response Time</h2>
                <p>With a 1ms MPRT response time, this monitor minimizes motion blur and ghosting, ensuring clear and sharp images during fast-paced action.</p>
                <h2>AMD FreeSync Technology</h2>
                <p>Equipped with AMD FreeSync, the G24C4 E2 synchronizes the monitor's refresh rate with your GPU, eliminating screen tearing and providing a fluid gaming experience.</p>
                <h2>Vibrant Colors</h2>
                <p>The VA panel delivers deep blacks and vibrant colors, enhancing the overall visual quality and making games and media content more lifelike.</p>
                <h2>Ergonomic Stand</h2>
                <p>The adjustable stand allows for tilt, swivel, and height adjustments, ensuring a comfortable and ergonomic viewing position during extended use.</p>""",
            "sale_id": None,
        },
        {
            "id": 131,
            "name": "Lenovo R27qe",
            "price": 299.99,
            "old_price": 379.99,
            "description": """<h2>27-Inch QHD IPS Display</h2>
                <p>The Lenovo R27qe boasts a 27-inch QHD (2560x1440) IPS display, delivering accurate colors and wide viewing angles for an exceptional visual experience.</p>
                <h2>High Refresh Rate</h2>
                <p>With a 165Hz refresh rate, this monitor ensures smooth and responsive gameplay, reducing motion blur and enhancing your gaming performance.</p>
                <h2>Adaptive Sync Technology</h2>
                <p>Featuring AMD FreeSync Premium, the R27qe synchronizes the monitor's refresh rate with your GPU, eliminating screen tearing and providing fluid visuals.</p>
                <h2>Low Input Lag</h2>
                <p>Designed for gamers, the R27qe offers low input lag and a fast response time of 1ms MPRT, ensuring your actions are displayed instantly on the screen.</p>
                <h2>Ergonomic Design</h2>
                <p>The adjustable stand allows you to tilt, swivel, and adjust the height of the monitor, providing a comfortable and ergonomic viewing angle for prolonged use.</p>""",
            "sale_id": None,
        },
        {
            "id": 132,
            "name": "MSI PRO MP251",
            "price": 199.99,
            "old_price": 239.99,
            "description": """<h2>24-Inch Full HD Display</h2>
                <p>The MSI PRO MP251 features a 24-inch Full HD (1920x1080) IPS display, offering sharp and clear visuals that enhance both work and entertainment experiences.</p>
                <h2>60Hz Refresh Rate</h2>
                <p>With a 60Hz refresh rate, this monitor provides smooth and stable visuals, making it ideal for office tasks, casual gaming, and multimedia consumption.</p>
                <h2>Eye Care Technology</h2>
                <p>Equipped with MSI's Eye Care technology, including flicker-free backlighting and a blue light filter, the MP251 reduces eye strain during extended use.</p>
                <h2>Slim Bezel Design</h2>
                <p>The slim bezel design minimizes distractions and allows for a seamless multi-monitor setup, perfect for enhancing your productivity and workspace aesthetics.</p>
                <h2>Ergonomic Adjustments</h2>
                <p>The adjustable stand offers tilt and swivel functions, allowing you to customize the viewing angle for maximum comfort and ergonomic support.</p>""",
            "sale_id": None,
        },
        {
            "id": 133,
            "name": "Gigabyte GS27Q",
            "price": 349.99,
            "old_price": 429.99,
            "description": """<h2>27-Inch QHD Gaming Monitor</h2>
                <p>The Gigabyte GS27Q features a 27-inch QHD (2560x1440) display with a 165Hz refresh rate, delivering crisp and detailed visuals that enhance your gaming and multimedia experiences.</p>
                <h2>Fast Response Time</h2>
                <p>With a 1ms MPRT response time, the GS27Q minimizes motion blur and ghosting, ensuring smooth and clear images during fast-paced action.</p>
                <h2>AMD FreeSync Premium</h2>
                <p>Experience tear-free gaming with AMD FreeSync Premium, which synchronizes the monitor's refresh rate with your GPU for fluid and uninterrupted visuals.</p>
                <h2>Wide Color Gamut</h2>
                <p>Featuring a 95% DCI-P3 color gamut, the GS27Q delivers vibrant and accurate colors, making it ideal for both gaming and professional content creation.</p>
                <h2>Ergonomic Stand and Design</h2>
                <p>The adjustable stand allows for tilt, swivel, and height adjustments, providing a comfortable and ergonomic viewing position. The sleek design with customizable RGB lighting adds a stylish touch to your setup.</p>""",
            "sale_id": None,
        },
        {
            "id": 134,
            "name": "LG 24MR400-B",
            "price": 179.99,
            "old_price": 219.99,
            "description": """<h2>24-Inch Full HD IPS Display</h2>
                <p>The LG 24MR400-B offers a 24-inch Full HD (1920x1080) IPS display, providing sharp and vibrant visuals with wide viewing angles for an enhanced viewing experience.</p>
                <h2>75Hz Refresh Rate</h2>
                <p>Enjoy smooth and fluid visuals with a 75Hz refresh rate, reducing motion blur and providing a more responsive experience during gaming and multimedia tasks.</p>
                <h2>AMD FreeSync Technology</h2>
                <p>Equipped with AMD FreeSync, the 24MR400-B synchronizes the monitor's refresh rate with your GPU, eliminating screen tearing and providing seamless gameplay.</p>
                <h2>Eye Comfort Features</h2>
                <p>LG's Flicker Safe and Reader Mode technologies reduce eye strain by minimizing screen flicker and adjusting blue light levels, making it ideal for long hours of use.</p>
                <h2>Ergonomic Design</h2>
                <p>The monitor features tilt adjustment, allowing you to customize the viewing angle for maximum comfort and ergonomic support during extended use.</p>""",
            "sale_id": None,
        },
        {
            "id": 135,
            "name": "Dell G2524H",
            "price": 249.99,
            "old_price": 299.99,
            "description": """<h2>24-Inch Gaming Monitor</h2>
                <p>The Dell G2524H features a 24-inch Full HD (1920x1080) display with a blazing 240Hz refresh rate, delivering ultra-smooth and responsive visuals that elevate your gaming experience.</p>
                <h2>Fast Response Time</h2>
                <p>With a 0.5ms (GtG) response time, this monitor ensures minimal motion blur and ghosting, providing clear and sharp images even during the most intense gaming moments.</p>
                <h2>AMD FreeSync Premium</h2>
                <p>Experience tear-free gaming with AMD FreeSync Premium, which dynamically adjusts the monitor's refresh rate to match your GPU, eliminating screen tearing and stuttering.</p>
                <h2>Vivid Color Accuracy</h2>
                <p>The IPS panel delivers vibrant and accurate colors with a 99% sRGB color gamut, enhancing both gaming and multimedia content for a more immersive experience.</p>
                <h2>Ergonomic and Stylish Design</h2>
                <p>The adjustable stand allows for tilt, swivel, and height adjustments, ensuring a comfortable and ergonomic viewing position. The sleek design with customizable RGB lighting adds a modern touch to your gaming setup.</p>""",
            "sale_id": None,
        },
        {
            "id": 136,
            "name": "Netgear Nighthawk RS500 (12000Mb/s a/b/g/n/ac/ax/be)",
            "price": 299.99,
            "old_price": 349.99,
            "description": """<h2>Ultra-Fast Wi-Fi 6E Technology</h2>
                <p>The Netgear Nighthawk RS500 leverages the latest Wi-Fi 6E standard, delivering blazing speeds up to 12000Mb/s across multiple bands (a/b/g/n/ac/ax/be) for seamless connectivity and superior performance.</p>
                <h2>Advanced Beamforming+</h2>
                <p>Enhanced beamforming+ technology ensures stronger and more reliable connections by directing Wi-Fi signals precisely to your devices, reducing dead zones and improving overall coverage.</h2>
                <h2>Robust Security Features</h2>
                <p>Equipped with Netgear Armor cybersecurity, the RS500 provides comprehensive protection against online threats, safeguarding your network and connected devices with advanced security protocols.</p>
                <h2>Multi-Gigabit Ethernet Ports</h2>
                <p>Featuring multi-gigabit Ethernet ports, the RS500 supports high-speed wired connections for gaming consoles, streaming devices, and other bandwidth-intensive applications, ensuring minimal latency and maximum throughput.</p>
                <h2>Intuitive Management with Nighthawk App</h2>
                <p>Manage your network effortlessly using the Nighthawk app, which offers easy setup, real-time monitoring, and advanced customization options to optimize your home or office network.</p>""",
            "sale_id": None,
        },
        {
            "id": 137,
            "name": "TP-Link Archer AX55 Pro (3000Mb/s a/b/g/n/ac/ax) USB 3.0",
            "price": 179.99,
            "old_price": 219.99,
            "description": """<h2>High-Speed Wi-Fi 6 Performance</h2>
                <p>The TP-Link Archer AX55 Pro delivers impressive speeds up to 3000Mb/s with Wi-Fi 6 (a/b/g/n/ac/ax) support, ensuring fast and reliable connections for all your devices.</p>
                <h2>Dual-Band Connectivity</h2>
                <p>Experience optimal performance with dual-band operation, allowing you to connect multiple devices simultaneously without compromising on speed or stability.</h2>
                <h2>USB 3.0 Ports for Versatile Connectivity</h2>
                <p>Equipped with USB 3.0 ports, the Archer AX55 Pro enables seamless connection of external storage devices, printers, and other peripherals, enhancing your network's functionality.</p>
                <h2>Advanced QoS and Beamforming</h2>
                <p>Quality of Service (QoS) prioritizes bandwidth for high-demand applications like gaming and streaming, while beamforming technology directs signals to your devices for enhanced coverage and performance.</p>
                <h2>Easy Setup and Management</h2>
                <p>Set up and manage your network effortlessly with the Tether app, offering user-friendly controls, real-time monitoring, and parental controls to ensure a secure and efficient network environment.</p>""",
            "sale_id": None,
        },
        {
            "id": 138,
            "name": "TP-Link Archer AX23 (1800Mb/s a/b/g/n/ac/ax)",
            "price": 129.99,
            "old_price": 159.99,
            "description": """<h2>Efficient Wi-Fi 6 Connectivity</h2>
                <p>The TP-Link Archer AX23 offers reliable Wi-Fi 6 (a/b/g/n/ac/ax) performance with speeds up to 1800Mb/s, providing fast and stable connections for your home network needs.</p>
                <h2>Compact and Stylish Design</h2>
                <p>Featuring a sleek and compact design, the Archer AX23 seamlessly blends into any home or office environment, offering both aesthetic appeal and practical functionality.</h2>
                <h2>Enhanced Coverage with Beamforming</h2>
                <p>Beamforming technology ensures that Wi-Fi signals are directed towards your devices, extending coverage and reducing dead spots for a more consistent internet experience.</p>
                <h2>Advanced Security with WPA3</h2>
                <p>Protect your network with the latest WPA3 security protocol, providing stronger encryption and enhanced protection against unauthorized access and cyber threats.</p>
                <h2>Easy Setup and Management</h2>
                <p>Utilize the Tether app for quick and easy setup, as well as ongoing network management, including device prioritization and parental controls to maintain a secure and efficient network.</p>""",
            "sale_id": None,
        },
        {
            "id": 139,
            "name": "TP-Link Archer BE230 (3600Mb/s a/b/g/n/ac/ax/be) USB 3.0",
            "price": 249.99,
            "old_price": 299.99,
            "description": """<h2>Tri-Band Wi-Fi 6 Performance</h2>
                <p>The TP-Link Archer BE230 delivers ultra-fast tri-band Wi-Fi 6 (a/b/g/n/ac/ax/be) speeds up to 3600Mb/s, ensuring seamless connectivity for all your high-bandwidth devices.</p>
                <h2>Dedicated Backhaul Band</h2>
                <p>With a dedicated backhaul band, the Archer BE230 maintains optimal speeds and reduces congestion, providing a stable and efficient network even with multiple connected devices.</h2>
                <h2>USB 3.0 Ports for Enhanced Connectivity</h2>
                <p>Equipped with USB 3.0 ports, this router allows for easy connection of external storage, printers, and other peripherals, expanding your network's capabilities.</p>
                <h2>Advanced Security Features</h2>
                <p>Protect your network with built-in security features, including WPA3 encryption and TP-Link HomeCare™, which offers antivirus protection, parental controls, and QoS prioritization.</p>
                <h2>Intuitive Setup and Management</h2>
                <p>Manage your network effortlessly using the Tether app, which provides a user-friendly interface for setup, monitoring, and optimizing your network performance.</p>""",
            "sale_id": None,
        },
        {
            "id": 140,
            "name": "TP-Link Archer C6 (1200Mb/s a/b/g/n/ac) DualBand",
            "price": 89.99,
            "old_price": 119.99,
            "description": """<h2>Reliable Dual-Band Wi-Fi</h2>
                <p>The TP-Link Archer C6 offers dependable Dual-Band (a/b/g/n/ac) Wi-Fi performance with speeds up to 1200Mb/s, ensuring fast and stable connections for your home or office devices.</p>
                <h2>Seamless Device Management</h2>
                <p>Manage your network effortlessly with the Tether app, which provides easy setup, real-time monitoring, and advanced settings to optimize your Wi-Fi experience.</h2>
                <h2>Advanced Security with WPA3</h2>
                <p>Keep your network secure with the latest WPA3 encryption standard, offering enhanced protection against unauthorized access and cyber threats.</p>
                <h2>Beamforming Technology</h2>
                <p>Beamforming technology directs Wi-Fi signals towards your devices, improving coverage and ensuring a more consistent and reliable connection throughout your space.</p>
                <h2>Ethernet Ports for Wired Connections</h2>
                <p>Featuring multiple Ethernet ports, the Archer C6 supports high-speed wired connections for gaming consoles, smart TVs, and other bandwidth-intensive devices.</p>""",
            "sale_id": None,
        },
        {
            "id": 141,
            "name": "ASUS RT-AX53U (1800Mb/s a/b/g/n/ac/ax, 1xUSB, 3xLAN)",
            "price": 159.99,
            "old_price": 199.99,
            "description": """<h2>Powerful Wi-Fi 6 Connectivity</h2>
                <p>The ASUS RT-AX53U delivers robust Wi-Fi 6 (a/b/g/n/ac/ax) performance with speeds up to 1800Mb/s, providing fast and reliable connections for all your devices.</p>
                <h2>Triple LAN Ports for Versatile Networking</h2>
                <p>Equipped with three Gigabit LAN ports, the RT-AX53U supports multiple wired connections for gaming consoles, smart TVs, and other high-speed devices.</h2>
                <h2>USB Connectivity for Expanded Functionality</h2>
                <p>Featuring a USB port, this router allows you to connect external storage devices or printers, enabling easy file sharing and peripheral connectivity across your network.</p>
                <h2>Advanced QoS and Beamforming</h2>
                <p>Quality of Service (QoS) prioritizes bandwidth for high-demand applications, while beamforming technology enhances signal strength and coverage, ensuring a smooth and efficient network experience.</p>
                <h2>Intuitive ASUS Router App</h2>
                <p>Manage your network with ease using the ASUS Router app, which offers simple setup, real-time monitoring, and advanced customization options to optimize your home or office network.</p>""",
            "sale_id": None,
        },
        {
            "id": 142,
            "name": "TP-Link MR200 750Mbps a/b/g/n/ac 3G/4G (LTE) 150Mbps 4xLAN",
            "price": 199.99,
            "old_price": 239.99,
            "description": """<h2>Versatile Dual-Band Wi-Fi</h2>
                <p>The TP-Link MR200 offers reliable Dual-Band (a/b/g/n/ac) Wi-Fi performance with speeds up to 750Mbps, ensuring fast and stable connections for all your devices.</p>
                <h2>Integrated 3G/4G LTE Support</h2>
                <p>Stay connected even during internet outages with built-in 3G/4G LTE support, providing a seamless fallback connection for uninterrupted internet access.</h2>
                <h2>High-Speed Wired Connections</h2>
                <p>Featuring four Gigabit LAN ports, the MR200 supports multiple wired connections for gaming consoles, smart TVs, and other high-speed devices, enhancing your network's versatility.</p>
                <h2>Advanced Security Features</h2>
                <p>Protect your network with WPA3 encryption and built-in firewall protection, ensuring your data and devices are safeguarded against unauthorized access and cyber threats.</p>
                <h2>Easy Setup and Management</h2>
                <p>Manage your network effortlessly using the Tether app, which provides intuitive controls, real-time monitoring, and advanced settings to optimize your Wi-Fi experience.</p>""",
            "sale_id": None,
        },
        {
            "id": 143,
            "name": "TP-Link Archer AX53 (3000Mb/s a/b/g/n/ac/ax)",
            "price": 229.99,
            "old_price": 279.99,
            "description": """<h2>Exceptional Wi-Fi 6 Performance</h2>
                <p>The TP-Link Archer AX53 delivers outstanding Wi-Fi 6 (a/b/g/n/ac/ax) performance with speeds up to 3000Mb/s, ensuring ultra-fast and reliable connections for all your devices.</p>
                <h2>Tri-Band Technology</h2>
                <p>Equipped with tri-band technology, the Archer AX53 offers dedicated bands for high-speed connections, reducing congestion and enhancing overall network efficiency.</h2>
                <h2>Advanced Beamforming+</h2>
                <p>Beamforming+ technology directs Wi-Fi signals towards your devices, improving coverage and ensuring a stronger and more stable connection throughout your home or office.</p>
                <h2>Comprehensive Security with WPA3</h2>
                <p>Protect your network with the latest WPA3 security protocol, providing enhanced encryption and safeguarding your data against unauthorized access and cyber threats.</p>
                <h2>Intuitive TP-Link Management</h2>
                <p>Manage your network effortlessly with the Tether app, offering easy setup, real-time monitoring, and advanced customization options to optimize your Wi-Fi experience.</p>""",
            "sale_id": None,
        },
        {
            "id": 144,
            "name": "TP-Link Archer NX200 5G 4,67Gbps (Wi-Fi 6 1800Mb/s a/b/g/n/ac/ax)",
            "price": 349.99,
            "old_price": 399.99,
            "description": """<h2>Cutting-Edge Wi-Fi 6 Technology</h2>
                <p>The TP-Link Archer NX200 leverages the latest Wi-Fi 6 (a/b/g/n/ac/ax) standards, delivering lightning-fast speeds up to 4.67Gbps, perfect for high-demand applications and multiple device connectivity.</p>
                <h2>Dedicated 5GHz Band</h2>
                <p>Enjoy unparalleled performance with a dedicated 5GHz band, reducing interference and ensuring stable and high-speed connections for gaming, streaming, and more.</h2>
                <h2>Advanced Beamforming</h2>
                <p>Beamforming technology directs Wi-Fi signals towards your devices, enhancing coverage and providing a more reliable and consistent connection throughout your space.</p>
                <h2>Multi-Gigabit Ethernet Ports</h2>
                <p>Featuring multi-gigabit Ethernet ports, the Archer NX200 supports ultra-fast wired connections for gaming consoles, smart TVs, and other high-speed devices, minimizing latency and maximizing throughput.</p>
                <h2>Robust Security Features</h2>
                <p>Protect your network with WPA3 encryption and built-in security features, ensuring your data and devices remain safe from unauthorized access and cyber threats.</p>""",
            "sale_id": None,
        },
        {
            "id": 145,
            "name": "ASUS RT-AX58U (3000Mb/s a/b/g/n/ac/ax, 1xUSB, 4xLAN)",
            "price": 279.99,
            "old_price": 329.99,
            "description": """<h2>Superior Wi-Fi 6 Performance</h2>
                <p>The ASUS RT-AX58U delivers exceptional Wi-Fi 6 (a/b/g/n/ac/ax) performance with speeds up to 3000Mb/s, ensuring fast and reliable connections for all your devices.</p>
                <h2>Quad LAN Ports for Enhanced Connectivity</h2>
                <p>Equipped with four Gigabit LAN ports, the RT-AX58U supports multiple wired connections for gaming consoles, smart TVs, and other high-speed devices, providing flexibility and high performance.</h2>
                <h2>USB 3.0 Port for Expanded Functionality</h2>
                <p>Featuring a USB 3.0 port, this router allows you to connect external storage devices or printers, enabling easy file sharing and peripheral connectivity across your network.</p>
                <h2>Advanced Beamforming and MU-MIMO</h2>
                <p>Advanced beamforming and MU-MIMO technology ensure that Wi-Fi signals are directed towards your devices, optimizing coverage and maintaining high-speed connections even with multiple devices connected.</p>
                <h2>Comprehensive Security with AiProtection</h2>
                <p>Protect your network with ASUS AiProtection, which offers advanced security features such as malware protection, parental controls, and intrusion prevention, keeping your data and devices safe.</p>""",
            "sale_id": None,
        },
        {
            "id": 146,
            "name": "Baseus USB-C - USB-C (PD 100W, 2m)",
            "price": 19.99,
            "old_price": 24.99,
            "description": """<h2>High-Speed Data Transfer</h2>
                <p>The Baseus USB-C to USB-C cable supports up to 100W Power Delivery (PD), enabling fast charging and efficient power delivery to your compatible devices.</p>
                <h2>Durable Braided Design</h2>
                <p>Featuring a robust braided exterior, this 2-meter cable ensures longevity and resistance to everyday wear and tear, making it ideal for both home and office use.</p>
                <h2>Universal Compatibility</h2>
                <p>Compatible with a wide range of USB-C devices, including smartphones, tablets, laptops, and more, providing versatile connectivity options for your tech needs.</p>
                <h2>Reliable Performance</h2>
                <p>Designed to deliver stable and consistent performance, the Baseus USB-C cable ensures seamless data transfer and reliable charging without interruptions.</p>
                <h2>Easy Plug-and-Play</h2>
                <p>The plug-and-play functionality allows for hassle-free setup, making it simple to connect and use with your USB-C enabled devices.</p>""",
            "sale_id": None,
        },
        {
            "id": 147,
            "name": "Silver Monkey Kabel HDMI 2.1 w oplocie 3m",
            "price": 29.99,
            "old_price": 34.99,
            "description": """<h2>Ultra High Definition</h2>
                <p>The Silver Monkey HDMI 2.1 cable supports 4K@120Hz and 8K@60Hz resolutions, delivering stunningly sharp and smooth visuals for your gaming and multimedia experiences.</p>
                <h2>Premium Braided Protection</h2>
                <p>Equipped with a durable braided sheath, this 3-meter HDMI cable resists tangling and enhances durability, ensuring long-lasting performance even with frequent use.</p>
                <h2>High Bandwidth Capability</h2>
                <p>With a bandwidth of up to 48Gbps, the Silver Monkey HDMI 2.1 cable ensures flawless transmission of high-resolution audio and video signals without lag or interference.</p>
                <h2>Backward Compatibility</h2>
                <p>Fully compatible with all previous HDMI versions, this cable seamlessly connects your older devices while providing the latest HDMI 2.1 features for future-proofing your setup.</p>
                <h2>Easy Installation</h2>
                <p>The slim and flexible design allows for easy installation in tight spaces, making it perfect for home theaters, gaming rigs, and office setups.</p>""",
            "sale_id": None,
        },
        {
            "id": 148,
            "name": "Silver Monkey Kabel USB-C 3.0 100W 1 m B",
            "price": 14.99,
            "old_price": 19.99,
            "description": """<h2>Fast Charging and Data Transfer</h2>
                <p>The Silver Monkey USB-C 3.0 cable delivers up to 100W Power Delivery (PD) for rapid charging of your devices, while supporting data transfer speeds of up to 5Gbps for efficient file sharing.</p>
                <h2>Compact and Portable</h2>
                <p>With a length of 1 meter, this USB-C cable is perfect for on-the-go use, fitting easily into your bag or pocket for convenient connectivity wherever you are.</p>
                <h2>Durable Construction</h2>
                <p>Designed with high-quality materials, the Silver Monkey USB-C cable ensures longevity and resilience against daily wear and tear, providing reliable performance over time.</p>
                <h2>Wide Compatibility</h2>
                <p>Compatible with a variety of USB-C devices, including smartphones, tablets, laptops, and peripherals, offering versatile connectivity options for all your gadgets.</p>
                <h2>Easy Plug-and-Play</h2>
                <p>Enjoy hassle-free setup with the plug-and-play design, allowing you to quickly connect and charge your devices without the need for additional software or drivers.</p>""",
            "sale_id": None,
        },
        {
            "id": 149,
            "name": "Silver Monkey Kabel DisplayPort 1.4 w oplocie 3m",
            "price": 24.99,
            "old_price": 29.99,
            "description": """<h2>High-Resolution Display</h2>
                <p>The Silver Monkey DisplayPort 1.4 cable supports up to 8K@60Hz and 4K@144Hz, providing crystal-clear and ultra-smooth visuals for your monitors and gaming setups.</p>
                <h2>Durable Braided Cable</h2>
                <p>Featuring a sturdy braided exterior, this 3-meter DisplayPort cable resists tangling and enhances durability, ensuring reliable performance even with frequent use.</p>
                <h2>Enhanced Signal Integrity</h2>
                <p>Advanced shielding techniques minimize interference and signal loss, delivering stable and high-quality audio and video transmission for an optimal viewing experience.</p>
                <h2>Backward Compatible</h2>
                <p>Fully compatible with previous DisplayPort versions, this cable seamlessly connects with older devices while providing the latest DisplayPort 1.4 features for future-proofing your setup.</p>
                <h2>Flexible and Easy to Install</h2>
                <p>The flexible design allows for easy installation in tight spaces, making it perfect for multi-monitor setups, home offices, and gaming rigs.</p>""",
            "sale_id": None,
        },
        {
            "id": 150,
            "name": "Silver Monkey Kabel DisplayPort 1.2 - HDMI 1.8m",
            "price": 19.99,
            "old_price": 24.99,
            "description": """<h2>Versatile Connectivity</h2>
                <p>The Silver Monkey DisplayPort 1.2 to HDMI cable enables seamless connection between your DisplayPort-enabled devices and HDMI displays, supporting high-definition audio and video transmission.</p>
                <h2>High-Resolution Support</h2>
                <p>Supports resolutions up to 4K@60Hz, ensuring sharp and vibrant visuals for your monitors, TVs, and projectors, enhancing your viewing and gaming experiences.</p>
                <h2>Durable Build Quality</h2>
                <p>Constructed with a robust braided cable, this 1.8-meter adapter resists tangling and wear, providing long-lasting performance and reliability.</p>
                <h2>Easy Plug-and-Play</h2>
                <p>No drivers or additional software required. Simply connect your devices and enjoy instant high-quality audio and video transmission.</p>
                <h2>Compact and Flexible Design</h2>
                <p>The slim and flexible design allows for easy installation in any setup, making it ideal for home theaters, gaming stations, and professional workspaces.</p>""",
            "sale_id": None,
        },
        {
            "id": 151,
            "name": "Silver Monkey Kabel USB-A na USB-C 1 m 45W",
            "price": 12.99,
            "old_price": 16.99,
            "description": """<h2>Reliable Charging Solution</h2>
                <p>The Silver Monkey USB-A to USB-C cable delivers up to 45W Power Delivery (PD), ensuring fast and efficient charging for your USB-C enabled devices, including smartphones, tablets, and laptops.</p>
                <h2>High-Speed Data Transfer</h2>
                <p>Supports data transfer speeds of up to 5Gbps, enabling quick and seamless file sharing between your devices without compromising on speed or reliability.</p>
                <h2>Durable and Tangle-Free</h2>
                <p>Featuring a sturdy braided exterior, this 1-meter cable resists tangling and enhances durability, providing long-lasting performance even with daily use.</p>
                <h2>Wide Compatibility</h2>
                <p>Compatible with a variety of USB-A and USB-C devices, offering versatile connectivity options for all your gadgets and peripherals.</p>
                <h2>Compact and Portable</h2>
                <p>The lightweight and compact design makes it easy to carry, perfect for on-the-go charging and data transfer needs.</p>""",
            "sale_id": None,
        },
        {
            "id": 152,
            "name": "Silver Monkey Adapter USB-C - minijack 3.5 W",
            "price": 9.99,
            "old_price": 12.99,
            "description": """<h2>Seamless Audio Connectivity</h2>
                <p>The Silver Monkey USB-C to Minijack adapter allows you to easily connect your USB-C devices to traditional 3.5mm audio headphones and speakers, ensuring versatile audio compatibility.</p>
                <h2>Compact and Portable</h2>
                <p>Designed for convenience, this compact adapter easily fits into your pocket or bag, making it perfect for on-the-go audio needs.</h2>
                <h2>High-Quality Sound</h2>
                <p>Delivers clear and balanced audio output, enhancing your listening experience with minimal signal loss and distortion.</p>
                <h2>Plug-and-Play Functionality</h2>
                <p>No drivers or additional software required. Simply plug in the adapter and enjoy instant audio connectivity.</p>
                <h2>Durable Construction</h2>
                <p>Built with high-quality materials, the Silver Monkey adapter ensures long-lasting durability and reliable performance for all your audio connections.</p>""",
            "sale_id": None,
        },
        {
            "id": 153,
            "name": "Silver Monkey Kabel RJ-45 - RJ-45 UTP kat.6 2m",
            "price": 14.99,
            "old_price": 19.99,
            "description": """<h2>High-Speed Ethernet Connectivity</h2>
                <p>The Silver Monkey RJ-45 UTP Cat.6 cable provides reliable and high-speed Ethernet connections, supporting data transfer rates up to 1Gbps for seamless networking and online experiences.</p>
                <h2>Durable Twisted Pair Construction</h2>
                <p>Featuring twisted pair wiring and high-quality connectors, this 2-meter cable minimizes interference and ensures stable and consistent network performance.</p>
                <h2>Flexible and Easy to Install</h2>
                <p>The flexible design allows for easy installation in tight spaces, making it ideal for home offices, gaming setups, and professional environments.</p>
                <h2>Shielded for Reduced Interference</h2>
                <p>Shielded design reduces electromagnetic interference (EMI) and crosstalk, ensuring a clear and uninterrupted network connection.</p>
                <h2>Wide Compatibility</h2>
                <p>Compatible with a variety of networking devices, including routers, switches, PCs, and gaming consoles, offering versatile connectivity solutions for all your networking needs.</p>""",
            "sale_id": None,
        },
        {
            "id": 154,
            "name": "Silver Monkey Kabel SATA III, kątowy, 0,5m czarny",
            "price": 9.99,
            "old_price": 12.99,
            "description": """<h2>Reliable Data Transfer</h2>
                <p>The Silver Monkey SATA III cable ensures fast and reliable data transfer rates up to 6Gbps, making it perfect for connecting your hard drives, SSDs, and optical drives to your motherboard.</p>
                <h2>Angled Connector Design</h2>
                <p>Featuring an angled connector, this 0.5-meter cable provides greater flexibility and ease of installation in tight spaces, reducing cable clutter and improving airflow within your PC case.</h2>
                <h2>Durable and Flexible</h2>
                <p>Constructed with high-quality materials, the angled SATA III cable is both durable and flexible, ensuring long-lasting performance and easy maneuverability during installation.</p>
                <h2>Easy Plug-and-Play</h2>
                <p>Designed for hassle-free setup, simply plug the cable into your SATA ports and enjoy instant high-speed data connectivity without the need for additional drivers or software.</p>
                <h2>Universal Compatibility</h2>
                <p>Compatible with all SATA III devices and motherboards, this cable offers versatile connectivity options for a wide range of storage solutions.</p>""",
            "sale_id": None,
        },
        {
            "id": 155,
            "name": "Silver Monkey Kabel SCHUKO - C13 1,8m",
            "price": 11.99,
            "old_price": 15.99,
            "description": """<h2>Reliable Power Connection</h2>
                <p>The Silver Monkey SCHUKO to C13 power cable provides a secure and stable power connection for your desktop computers, servers, and other electronic devices requiring a reliable power source.</p>
                <h2>High-Quality Construction</h2>
                <p>Built with durable materials and reinforced connectors, this 1.8-meter power cable ensures long-lasting performance and safety for all your power needs.</h2>
                <h2>Flexible and Tangle-Free</h2>
                <p>The flexible design allows for easy routing and management of cables, preventing tangling and reducing clutter in your workspace or server rack.</p>
                <h2>Safe and Compliant</h2>
                <p>Certified for safety and compliance with international standards, the Silver Monkey SCHUKO to C13 cable guarantees protection against electrical faults and ensures safe operation.</p>
                <h2>Universal Compatibility</h2>
                <p>Compatible with a wide range of devices featuring C13 power inputs, including desktops, monitors, printers, and networking equipment, offering versatile power connectivity solutions.</p>""",
            "sale_id": None,
        }
    ]

    for product_data in products:
        try:
            sale = Sale.objects.get(id=product_data["sale_id"]) if product_data["sale_id"] else None
            Product.objects.create(
                id=product_data["id"],
                name=product_data["name"],
                price=product_data["price"],
                old_price=product_data["old_price"],
                description=product_data["description"],
                sale=sale,
            )
            print(Fore.GREEN + f"Successfully added product: {product_data['name']}")
        except Sale.DoesNotExist:
            print(Fore.RED + f"Sale with ID {product_data['sale_id']} does not exist. Skipping product: {product_data['name']}.")
        except Exception as e:
            print(Fore.RED + f"Error adding product {product_data['name']}: {e}")

    print(Fore.GREEN + "Products successfully seeded.")

def seed_product_photos():
    PhotoProduct.objects.all().delete()

    photo_data = [
        {"id": 1, "product_id": 1, "path": "computer1.webp"},

        {"id": 2, "product_id": 2, "path": "computer2.webp"},

        {"id": 3, "product_id": 3, "path": "computer3.webp"},

        {"id": 4, "product_id": 4, "path": "computer4.webp"},

        {"id": 5, "product_id": 5, "path": "computer5.webp"},

        {"id": 6, "product_id": 6, "path": "computer6.webp"},

        {"id": 7, "product_id": 7, "path": "computer7.webp"},

        {"id": 8, "product_id": 8, "path": "computer8.webp"},

        {"id": 9, "product_id": 9, "path": "computer9.webp"},

        {"id": 10, "product_id": 10, "path": "laptop1v1.webp"},
        {"id": 11, "product_id": 10, "path": "laptop1v2.webp"},

        {"id": 12, "product_id": 11, "path": "laptop2v1.webp"},
        {"id": 13, "product_id": 11, "path": "laptop2v2.webp"},
        {"id": 14, "product_id": 11, "path": "laptop2v3.webp"},
        {"id": 15, "product_id": 11, "path": "laptop2v4.webp"},
        {"id": 16, "product_id": 11, "path": "laptop2v5.webp"},
        {"id": 17, "product_id": 11, "path": "laptop2v6.webp"},
        {"id": 18, "product_id": 11, "path": "laptop2v7.webp"},

        {"id": 19, "product_id": 12, "path": "laptop3v1.webp"},
        {"id": 20, "product_id": 12, "path": "laptop3v2.webp"},
        {"id": 21, "product_id": 12, "path": "laptop3v3.webp"},
        {"id": 22, "product_id": 12, "path": "laptop3v4.webp"},
        {"id": 23, "product_id": 12, "path": "laptop3v5.webp"},
        {"id": 24, "product_id": 12, "path": "laptop3v6.webp"},

        {"id": 25, "product_id": 13, "path": "laptop4v1.webp"},
        {"id": 26, "product_id": 13, "path": "laptop4v2.webp"},
        {"id": 27, "product_id": 13, "path": "laptop4v3.webp"},
        {"id": 28, "product_id": 13, "path": "laptop4v4.webp"},
        {"id": 29, "product_id": 13, "path": "laptop4v5.webp"},
        {"id": 30, "product_id": 13, "path": "laptop4v6.webp"},
        {"id": 31, "product_id": 13, "path": "laptop4v7.webp"},

        {"id": 32, "product_id": 14, "path": "laptop5v1.webp"},
        {"id": 33, "product_id": 14, "path": "laptop5v2.jpg"},
        {"id": 34, "product_id": 14, "path": "laptop5v3.webp"},
        {"id": 35, "product_id": 14, "path": "laptop5v4.jpg"},
        {"id": 36, "product_id": 14, "path": "laptop5v5.jpg"},
        {"id": 37, "product_id": 14, "path": "laptop5v6.webp"},

        {"id": 38, "product_id": 15, "path": "laptop7v1.webp"},
        {"id": 39, "product_id": 15, "path": "laptop7v2.webp"},
        {"id": 40, "product_id": 15, "path": "laptop7v3.webp"},
        {"id": 41, "product_id": 15, "path": "laptop7v4.webp"},
        {"id": 42, "product_id": 15, "path": "laptop7v5.webp"},

        {"id": 43, "product_id": 16, "path": "laptop8v1.webp"},
        {"id": 44, "product_id": 16, "path": "laptop8v2.webp"},
        {"id": 45, "product_id": 16, "path": "laptop8v3.webp"},
        {"id": 46, "product_id": 16, "path": "laptop8v4.webp"},
        {"id": 47, "product_id": 16, "path": "laptop8v5.webp"},
        {"id": 48, "product_id": 16, "path": "laptop8v6.webp"},

        {"id": 49, "product_id": 17, "path": "laptop9v1.webp"},
        {"id": 50, "product_id": 17, "path": "laptop9v2.jpg"},
        {"id": 51, "product_id": 17, "path": "laptop9v3.webp"},
        {"id": 52, "product_id": 17, "path": "laptop9v4.jpg"},
        {"id": 53, "product_id": 17, "path": "laptop9v5.jpg"},
        {"id": 54, "product_id": 17, "path": "laptop9v6.webp"},

        {"id": 55, "product_id": 18, "path": "laptop10v1.webp"},
        {"id": 56, "product_id": 18, "path": "laptop10v2.webp"},
        {"id": 57, "product_id": 18, "path": "laptop10v3.webp"},
        {"id": 58, "product_id": 18, "path": "laptop10v4.webp"},
        {"id": 59, "product_id": 18, "path": "laptop10v5.webp"},
        {"id": 60, "product_id": 18, "path": "laptop10v6.webp"},

        {"id": 61, "product_id": 19, "path": "laptop10v1.webp"},
        {"id": 62, "product_id": 19, "path": "laptop10v2.webp"},
        {"id": 63, "product_id": 19, "path": "laptop10v3.webp"},
        {"id": 64, "product_id": 19, "path": "laptop10v4.webp"},
        {"id": 65, "product_id": 19, "path": "laptop10v5.webp"},
        {"id": 66, "product_id": 19, "path": "laptop10v6.webp"},

        {"id": 67, "product_id": 20, "path": "case1v1.webp"},
        {"id": 68, "product_id": 20, "path": "case1v2.webp"},
        {"id": 69, "product_id": 20, "path": "case1v3.webp"},
        {"id": 70, "product_id": 20, "path": "case1v4.webp"},
        {"id": 71, "product_id": 20, "path": "case1v5.webp"},
        {"id": 72, "product_id": 20, "path": "case1v6.webp"},
        {"id": 73, "product_id": 20, "path": "case1v7.webp"},
        {"id": 74, "product_id": 20, "path": "case1v8.webp"},
        {"id": 75, "product_id": 20, "path": "case1v9.webp"},
        {"id": 76, "product_id": 20, "path": "case1v10.webp"},
        {"id": 77, "product_id": 20, "path": "case1v11.webp"},

        {"id": 78, "product_id": 21, "path": "case2v1.webp"},
        {"id": 79, "product_id": 21, "path": "case2v2.webp"},
        {"id": 80, "product_id": 21, "path": "case2v3.webp"},
        {"id": 81, "product_id": 21, "path": "case2v4.webp"},
        {"id": 82, "product_id": 21, "path": "case2v5.webp"},
        {"id": 83, "product_id": 21, "path": "case2v6.webp"},
        {"id": 84, "product_id": 21, "path": "case2v7.webp"},
        {"id": 85, "product_id": 21, "path": "case2v8.webp"},
        {"id": 86, "product_id": 21, "path": "case2v9.webp"},
        {"id": 87, "product_id": 21, "path": "case2v10.webp"},

        {"id": 88, "product_id": 22, "path": "case3v1.webp"},
        {"id": 89, "product_id": 22, "path": "case3v2.webp"},
        {"id": 90, "product_id": 22, "path": "case3v3.webp"},
        {"id": 91, "product_id": 22, "path": "case3v4.webp"},
        {"id": 92, "product_id": 22, "path": "case3v5.webp"},
        {"id": 93, "product_id": 22, "path": "case3v6.webp"},
        {"id": 94, "product_id": 22, "path": "case3v7.webp"},
        {"id": 95, "product_id": 22, "path": "case3v8.webp"},
        {"id": 96, "product_id": 22, "path": "case3v9.webp"},
        {"id": 97, "product_id": 22, "path": "case3v10.webp"},
        {"id": 98, "product_id": 22, "path": "case3v11.webp"},

        {"id": 99, "product_id": 23, "path": "case4v1.webp"},
        {"id": 100, "product_id": 23, "path": "case4v2.webp"},
        {"id": 101, "product_id": 23, "path": "case4v3.webp"},
        {"id": 102, "product_id": 23, "path": "case4v4.webp"},
        {"id": 103, "product_id": 23, "path": "case4v5.webp"},
        {"id": 104, "product_id": 23, "path": "case4v6.webp"},
        {"id": 105, "product_id": 23, "path": "case4v7.webp"},
        {"id": 106, "product_id": 23, "path": "case4v8.webp"},

        {"id": 107, "product_id": 24, "path": "case5v1.webp"},
        {"id": 108, "product_id": 24, "path": "case5v2.webp"},
        {"id": 109, "product_id": 24, "path": "case5v3.webp"},
        {"id": 110, "product_id": 24, "path": "case5v4.webp"},
        {"id": 111, "product_id": 24, "path": "case5v5.webp"},
        {"id": 112, "product_id": 24, "path": "case5v6.webp"},
        {"id": 113, "product_id": 24, "path": "case5v7.webp"},
        {"id": 114, "product_id": 24, "path": "case5v8.webp"},
        {"id": 115, "product_id": 24, "path": "case5v9.webp"},
        {"id": 116, "product_id": 24, "path": "case5v10.webp"},

        {"id": 117, "product_id": 25, "path": "case6v1.webp"},
        {"id": 118, "product_id": 25, "path": "case6v2.webp"},
        {"id": 119, "product_id": 25, "path": "case6v3.webp"},
        {"id": 120, "product_id": 25, "path": "case6v4.webp"},
        {"id": 121, "product_id": 25, "path": "case6v5.webp"},
        {"id": 122, "product_id": 25, "path": "case6v6.webp"},
        {"id": 123, "product_id": 25, "path": "case6v7.webp"},
        {"id": 124, "product_id": 25, "path": "case6v8.webp"},
        {"id": 125, "product_id": 25, "path": "case6v9.webp"},

        {"id": 126, "product_id": 26, "path": "case7v1.webp"},
        {"id": 127, "product_id": 26, "path": "case7v2.webp"},
        {"id": 128, "product_id": 26, "path": "case7v3.webp"},
        {"id": 129, "product_id": 26, "path": "case7v4.webp"},
        {"id": 130, "product_id": 26, "path": "case7v5.webp"},
        {"id": 131, "product_id": 26, "path": "case7v6.webp"},
        {"id": 132, "product_id": 26, "path": "case7v7.webp"},
        {"id": 133, "product_id": 26, "path": "case7v8.webp"},
        {"id": 134, "product_id": 26, "path": "case7v9.webp"},

        {"id": 135, "product_id": 27, "path": "case8v1.webp"},
        {"id": 136, "product_id": 27, "path": "case8v2.webp"},
        {"id": 137, "product_id": 27, "path": "case8v3.webp"},
        {"id": 138, "product_id": 27, "path": "case8v4.webp"},
        {"id": 139, "product_id": 27, "path": "case8v5.webp"},
        {"id": 140, "product_id": 27, "path": "case8v6.webp"},
        {"id": 141, "product_id": 27, "path": "case8v7.webp"},
        {"id": 142, "product_id": 27, "path": "case8v8.webp"},
        {"id": 143, "product_id": 27, "path": "case8v9.webp"},

        {"id": 144, "product_id": 28, "path": "case9v1.webp"},
        {"id": 145, "product_id": 28, "path": "case9v2.webp"},
        {"id": 146, "product_id": 28, "path": "case9v3.webp"},
        {"id": 147, "product_id": 28, "path": "case9v4.webp"},
        {"id": 148, "product_id": 28, "path": "case9v5.webp"},
        {"id": 149, "product_id": 28, "path": "case9v6.webp"},
        {"id": 150, "product_id": 28, "path": "case9v7.webp"},
        {"id": 151, "product_id": 28, "path": "case9v8.webp"},
        {"id": 152, "product_id": 28, "path": "case9v9.webp"},
        {"id": 153, "product_id": 28, "path": "case9v10.webp"},

        {"id": 154, "product_id": 29, "path": "aio1v1.webp"},
        {"id": 155, "product_id": 29, "path": "aio1v2.webp"},
        {"id": 156, "product_id": 29, "path": "aio1v3.webp"},
        {"id": 157, "product_id": 29, "path": "aio1v4.webp"},
        {"id": 158, "product_id": 29, "path": "aio1v5.webp"},
        {"id": 159, "product_id": 29, "path": "aio1v6.webp"},
        {"id": 160, "product_id": 29, "path": "aio1v7.webp"},
        {"id": 161, "product_id": 29, "path": "aio1v8.webp"},

        {"id": 162, "product_id": 30, "path": "aio2v1.webp"},
        {"id": 163, "product_id": 30, "path": "aio2v2.webp"},
        {"id": 164, "product_id": 30, "path": "aio2v3.webp"},
        {"id": 165, "product_id": 30, "path": "aio2v4.webp"},
        {"id": 166, "product_id": 30, "path": "aio2v5.webp"},
        {"id": 167, "product_id": 30, "path": "aio2v6.webp"},

        {"id": 168, "product_id": 31, "path": "aio3v1.webp"},
        {"id": 169, "product_id": 31, "path": "aio3v2.webp"},
        {"id": 170, "product_id": 31, "path": "aio3v3.webp"},
        {"id": 171, "product_id": 31, "path": "aio3v4.webp"},
        {"id": 172, "product_id": 31, "path": "aio3v5.webp"},
        {"id": 173, "product_id": 31, "path": "aio3v6.webp"},

        {"id": 174, "product_id": 32, "path": "aio4v1.webp"},
        {"id": 175, "product_id": 32, "path": "aio4v2.webp"},
        {"id": 176, "product_id": 32, "path": "aio4v3.webp"},
        {"id": 177, "product_id": 32, "path": "aio4v4.webp"},
        {"id": 178, "product_id": 32, "path": "aio4v5.webp"},
        {"id": 179, "product_id": 32, "path": "aio4v6.webp"},
        {"id": 180, "product_id": 32, "path": "aio4v7.webp"},
        {"id": 181, "product_id": 32, "path": "aio4v8.webp"},

        {"id": 182, "product_id": 33, "path": "aio5v1.webp"},
        {"id": 183, "product_id": 33, "path": "aio5v2.webp"},
        {"id": 184, "product_id": 33, "path": "aio5v3.webp"},
        {"id": 185, "product_id": 33, "path": "aio5v4.webp"},
        {"id": 186, "product_id": 33, "path": "aio5v5.webp"},
        {"id": 187, "product_id": 33, "path": "aio5v6.webp"},
        {"id": 188, "product_id": 33, "path": "aio5v7.webp"},
        {"id": 189, "product_id": 33, "path": "aio5v8.webp"},
        
        {"id": 190, "product_id": 34, "path": "air1v1.webp"},
        {"id": 191, "product_id": 34, "path": "air1v2.webp"},
        {"id": 192, "product_id": 34, "path": "air1v3.webp"},
        {"id": 193, "product_id": 34, "path": "air1v4.webp"},
        {"id": 194, "product_id": 34, "path": "air1v5.webp"},
        {"id": 195, "product_id": 34, "path": "air1v6.webp"},
        
        {"id": 196, "product_id": 35, "path": "air2v1.webp"},
        {"id": 197, "product_id": 35, "path": "air2v2.webp"},
        {"id": 198, "product_id": 35, "path": "air2v3.webp"},
        {"id": 199, "product_id": 35, "path": "air2v4.webp"},
        {"id": 200, "product_id": 35, "path": "air2v5.webp"},
        {"id": 201, "product_id": 35, "path": "air2v6.webp"},
        {"id": 202, "product_id": 35, "path": "air2v7.webp"},
        {"id": 203, "product_id": 35, "path": "air2v8.webp"},
        {"id": 204, "product_id": 35, "path": "air2v9.webp"},
        
        {"id": 205, "product_id": 36, "path": "air3v1.webp"},
        {"id": 206, "product_id": 36, "path": "air3v2.webp"},
        {"id": 207, "product_id": 36, "path": "air3v3.webp"},
        {"id": 208, "product_id": 36, "path": "air3v4.webp"},
        {"id": 209, "product_id": 36, "path": "air3v5.webp"},
        {"id": 210, "product_id": 36, "path": "air3v6.webp"},
        
        {"id": 211, "product_id": 37, "path": "air4v1.webp"},
        {"id": 212, "product_id": 37, "path": "air4v2.webp"},
        {"id": 213, "product_id": 37, "path": "air4v3.webp"},
        {"id": 214, "product_id": 37, "path": "air4v4.webp"},
        
        {"id": 215, "product_id": 38, "path": "air5v1.webp"},
        {"id": 216, "product_id": 38, "path": "air5v2.webp"},
        {"id": 217, "product_id": 38, "path": "air5v3.webp"},
        {"id": 218, "product_id": 38, "path": "air5v4.webp"},
        {"id": 219, "product_id": 38, "path": "air5v5.webp"},
        {"id": 220, "product_id": 38, "path": "air5v6.webp"},
        {"id": 221, "product_id": 38, "path": "air5v7.webp"},
        {"id": 222, "product_id": 38, "path": "air5v8.webp"},
        {"id": 223, "product_id": 38, "path": "air5v9.webp"},
        {"id": 224, "product_id": 38, "path": "air5v10.webp"},
        
        {"id": 225, "product_id": 39, "path": "m2_2v1.webp"},
        {"id": 226, "product_id": 39, "path": "m2_2v2.webp"},
        {"id": 227, "product_id": 39, "path": "m2_2v3.webp"},
        {"id": 228, "product_id": 39, "path": "m2_2v4.webp"},
        {"id": 229, "product_id": 39, "path": "m2_2v5.webp"},
        {"id": 230, "product_id": 39, "path": "m2_2v6.webp"},
        
        {"id": 231, "product_id": 40, "path": "m2_3v1.webp"},
        {"id": 232, "product_id": 40, "path": "m2_3v2.webp"},
        {"id": 233, "product_id": 40, "path": "m2_3v3.webp"},
        {"id": 234, "product_id": 40, "path": "m2_3v4.webp"},
        {"id": 235, "product_id": 40, "path": "m2_3v5.webp"},
        {"id": 236, "product_id": 40, "path": "m2_3v6.webp"},
        
        {"id": 237, "product_id": 41, "path": "m2_4v1.webp"},
        {"id": 238, "product_id": 41, "path": "m2_4v2.webp"},
        {"id": 239, "product_id": 41, "path": "m2_4v3.webp"},
        {"id": 240, "product_id": 41, "path": "m2_4v4.webp"},
        {"id": 241, "product_id": 41, "path": "m2_4v5.webp"},
        {"id": 242, "product_id": 41, "path": "m2_4v6.webp"},
        {"id": 243, "product_id": 41, "path": "m2_4v7.webp"},
       
        {"id": 244, "product_id": 42, "path": "m2_5v1.webp"},
        {"id": 245, "product_id": 42, "path": "m2_5v2.webp"},
        {"id": 246, "product_id": 42, "path": "m2_5v3.webp"},
        {"id": 247, "product_id": 42, "path": "m2_5v4.webp"},
        {"id": 248, "product_id": 42, "path": "m2_5v5.webp"},
       
        {"id": 249, "product_id": 43, "path": "m2_6v1.webp"},
        {"id": 250, "product_id": 43, "path": "m2_6v2.webp"},
        {"id": 251, "product_id": 43, "path": "m2_6v3.webp"},
        {"id": 252, "product_id": 43, "path": "m2_6v4.webp"},
        {"id": 253, "product_id": 43, "path": "m2_6v5.webp"},
       
        {"id": 254, "product_id": 44, "path": "m2v1.webp"},
        
        {"id": 255, "product_id": 45, "path": "m2_8v1.webp"},
        {"id": 256, "product_id": 45, "path": "m2_8v2.webp"},
        {"id": 257, "product_id": 45, "path": "m2_8v3.webp"},
        
        {"id": 258, "product_id": 46, "path": "m2_9v1.webp"},
        {"id": 259, "product_id": 46, "path": "m2_9v2.webp"},
        
        {"id": 260, "product_id": 47, "path": "m2_7v1.webp"},
        {"id": 261, "product_id": 47, "path": "m2_7v2.webp"},
        {"id": 262, "product_id": 47, "path": "m2_7v3.webp"},
        
        {"id": 263, "product_id": 48, "path": "fan1v1.webp"},
        {"id": 264, "product_id": 48, "path": "fan1v2.webp"},
        {"id": 265, "product_id": 48, "path": "fan1v3.webp"},
        {"id": 266, "product_id": 48, "path": "fan1v4.webp"},
        {"id": 267, "product_id": 48, "path": "fan1v5.webp"},
        {"id": 268, "product_id": 48, "path": "fan1v6.webp"},
        
        {"id": 269, "product_id": 49, "path": "fan2v1.webp"},
        {"id": 270, "product_id": 49, "path": "fan2v2.webp"},
        {"id": 271, "product_id": 49, "path": "fan2v3.webp"},
        {"id": 272, "product_id": 49, "path": "fan2v4.webp"},
        {"id": 273, "product_id": 49, "path": "fan2v5.webp"},
        {"id": 274, "product_id": 49, "path": "fan2v6.webp"},
        
        {"id": 275, "product_id": 50, "path": "fan3v1.webp"},
        {"id": 276, "product_id": 50, "path": "fan3v2.webp"},
        {"id": 277, "product_id": 50, "path": "fan3v3.webp"},
        {"id": 278, "product_id": 50, "path": "fan3v4.webp"},
        
        {"id": 279, "product_id": 51, "path": "fan4v1.webp"},
        {"id": 280, "product_id": 51, "path": "fan4v2.webp"},
        {"id": 281, "product_id": 51, "path": "fan4v3.webp"},
        {"id": 282, "product_id": 51, "path": "fan4v4.webp"},
        
        {"id": 283, "product_id": 52, "path": "fan5v1.webp"},
        {"id": 284, "product_id": 52, "path": "fan5v2.webp"},
        {"id": 285, "product_id": 52, "path": "fan5v3.webp"},
        {"id": 286, "product_id": 52, "path": "fan5v4.webp"},
        
        {"id": 287, "product_id": 53, "path": "fan6v1.webp"},
        {"id": 288, "product_id": 53, "path": "fan6v2.webp"},
        {"id": 289, "product_id": 53, "path": "fan6v3.webp"},
        {"id": 290, "product_id": 53, "path": "fan6v4.webp"},
        {"id": 291, "product_id": 53, "path": "fan6v5.webp"},
        
        {"id": 292, "product_id": 54, "path": "fan7v1.webp"},
        {"id": 293, "product_id": 54, "path": "fan7v2.webp"},
        {"id": 294, "product_id": 54, "path": "fan7v3.webp"},
        {"id": 295, "product_id": 54, "path": "fan7v4.webp"},
        {"id": 296, "product_id": 54, "path": "fan7v5.webp"},
        
        {"id": 297, "product_id": 55, "path": "fan8v1.webp"},
        {"id": 298, "product_id": 55, "path": "fan8v2.webp"},
        {"id": 299, "product_id": 55, "path": "fan8v3.webp"},
        {"id": 300, "product_id": 55, "path": "fan8v4.webp"},
        {"id": 301, "product_id": 55, "path": "fan8v5.webp"},
        {"id": 302, "product_id": 55, "path": "fan8v6.webp"},
        
        {"id": 303, "product_id": 56, "path": "fan9v1.webp"},
        {"id": 304, "product_id": 56, "path": "fan9v2.webp"},
        {"id": 305, "product_id": 56, "path": "fan9v3.webp"},
        {"id": 306, "product_id": 56, "path": "fan9v4.webp"},
        {"id": 307, "product_id": 56, "path": "fan9v5.webp"},
        {"id": 308, "product_id": 56, "path": "fan9v6.jpg"},
        {"id": 309, "product_id": 56, "path": "fan9v7.webp"},
        
        {"id": 310, "product_id": 57, "path": "grap1v1.webp"},
        {"id": 311, "product_id": 57, "path": "grap1v2.webp"},
        {"id": 312, "product_id": 57, "path": "grap1v3.webp"},
        {"id": 313, "product_id": 57, "path": "grap1v4.webp"},
        {"id": 314, "product_id": 57, "path": "grap1v5.webp"},
        {"id": 315, "product_id": 57, "path": "grap1v6.webp"},
        
        {"id": 316, "product_id": 58, "path": "grap2v1.webp"},
        {"id": 317, "product_id": 58, "path": "grap2v2.webp"},
        {"id": 318, "product_id": 58, "path": "grap2v3.webp"},
        {"id": 319, "product_id": 58, "path": "grap2v4.webp"},
        {"id": 320, "product_id": 58, "path": "grap2v5.webp"},
        {"id": 321, "product_id": 58, "path": "grap2v6.webp"},
        
        {"id": 322, "product_id": 59, "path": "grap3v1.webp"},
        {"id": 323, "product_id": 59, "path": "grap3v2.webp"},
        {"id": 324, "product_id": 59, "path": "grap3v3.webp"},
        {"id": 325, "product_id": 59, "path": "grap3v4.webp"},
        {"id": 326, "product_id": 59, "path": "grap3v5.webp"},
        {"id": 327, "product_id": 59, "path": "grap3v6.webp"},
        {"id": 328, "product_id": 59, "path": "grap3v7.webp"},
        
        {"id": 329, "product_id": 60, "path": "grap4v1.webp"},
        {"id": 330, "product_id": 60, "path": "grap4v2.webp"},
        {"id": 331, "product_id": 60, "path": "grap4v3.webp"},
        {"id": 332, "product_id": 60, "path": "grap4v4.webp"},
        {"id": 333, "product_id": 60, "path": "grap4v5.webp"},
        {"id": 334, "product_id": 60, "path": "grap4v6.webp"},
        
        {"id": 335, "product_id": 61, "path": "grap5v1.webp"},
        {"id": 336, "product_id": 61, "path": "grap5v2.webp"},
        {"id": 337, "product_id": 61, "path": "grap5v3.webp"},
        {"id": 338, "product_id": 61, "path": "grap5v4.webp"},
        {"id": 339, "product_id": 61, "path": "grap5v5.webp"},
        {"id": 340, "product_id": 61, "path": "grap5v6.webp"},
        
        {"id": 341, "product_id": 62, "path": "grap6v1.webp"},
        {"id": 342, "product_id": 62, "path": "grap6v2.webp"},
        {"id": 343, "product_id": 62, "path": "grap6v3.webp"},
        {"id": 344, "product_id": 62, "path": "grap6v4.webp"},
        {"id": 345, "product_id": 62, "path": "grap6v5.webp"},
        {"id": 346, "product_id": 62, "path": "grap6v6.webp"},
        
        {"id": 347, "product_id": 63, "path": "grap7v1.webp"},
        {"id": 348, "product_id": 63, "path": "grap7v2.webp"},
        {"id": 349, "product_id": 63, "path": "grap7v3.webp"},
        {"id": 350, "product_id": 63, "path": "grap7v4.webp"},
        
        {"id": 351, "product_id": 64, "path": "grap8v1.webp"},
        {"id": 352, "product_id": 64, "path": "grap8v2.webp"},
        {"id": 353, "product_id": 64, "path": "grap8v3.webp"},
        {"id": 354, "product_id": 64, "path": "grap8v4.webp"},
        {"id": 355, "product_id": 64, "path": "grap8v5.webp"},
        {"id": 356, "product_id": 64, "path": "grap8v6.webp"},
        
        {"id": 357, "product_id": 65, "path": "grap9v1.webp"},
        {"id": 358, "product_id": 65, "path": "grap9v2.webp"},
        {"id": 359, "product_id": 65, "path": "grap9v3.webp"},
        {"id": 360, "product_id": 65, "path": "grap9v4.webp"},
        {"id": 361, "product_id": 65, "path": "grap9v5.webp"},
        {"id": 362, "product_id": 65, "path": "grap9v6.webp"},
        
        {"id": 363, "product_id": 66, "path": "grap10v1.webp"},
        {"id": 364, "product_id": 66, "path": "grap10v2.webp"},
        {"id": 365, "product_id": 66, "path": "grap10v3.webp"},
        {"id": 366, "product_id": 66, "path": "grap10v4.webp"},
        {"id": 367, "product_id": 66, "path": "grap10v5.webp"},
        {"id": 368, "product_id": 66, "path": "grap10v6.webp"},
        
        {"id": 369, "product_id": 67, "path": "ram1v1.webp"},
        {"id": 370, "product_id": 67, "path": "ram1v2.webp"},
        
        {"id": 371, "product_id": 68, "path": "ram2v1.webp"},
        {"id": 372, "product_id": 68, "path": "ram2v2.webp"},
        {"id": 373, "product_id": 68, "path": "ram2v3.webp"},
        
        {"id": 374, "product_id": 69, "path": "ram3v1.webp"},
        {"id": 375, "product_id": 69, "path": "ram3v2.webp"},
        {"id": 376, "product_id": 69, "path": "ram3v3.webp"},
        
        {"id": 377, "product_id": 70, "path": "ram4v1.webp"},
        {"id": 378, "product_id": 70, "path": "ram4v2.webp"},
        
        {"id": 379, "product_id": 71, "path": "ram5v1.webp"},
        {"id": 380, "product_id": 71, "path": "ram5v2.webp"},
        {"id": 381, "product_id": 71, "path": "ram5v3.webp"},
        
        {"id": 382, "product_id": 72, "path": "ram6v1.webp"},
        {"id": 383, "product_id": 72, "path": "ram6v2.webp"},
        {"id": 384, "product_id": 72, "path": "ram6v3.webp"},
        {"id": 385, "product_id": 72, "path": "ram6v4.webp"},
        
        {"id": 386, "product_id": 73, "path": "ram7v1.webp"},
        {"id": 387, "product_id": 73, "path": "ram7v2.webp"},
        {"id": 388, "product_id": 73, "path": "ram7v3.webp"},
        
        {"id": 389, "product_id": 74, "path": "ram8v1.webp"},
        {"id": 390, "product_id": 74, "path": "ram8v2.webp"},
        {"id": 391, "product_id": 74, "path": "ram8v3.webp"},
        {"id": 392, "product_id": 74, "path": "ram8v4.webp"},
        {"id": 393, "product_id": 74, "path": "ram8v5.webp"},
        {"id": 394, "product_id": 74, "path": "ram8v6.webp"},
        
        {"id": 395, "product_id": 75, "path": "ram9v1.webp"},
        {"id": 396, "product_id": 75, "path": "ram9v2.webp"},
        {"id": 397, "product_id": 75, "path": "ram9v3.webp"},
        {"id": 398, "product_id": 75, "path": "ram9v4.webp"},
        
        {"id": 399, "product_id": 76, "path": "ram10v1.webp"},
        {"id": 400, "product_id": 76, "path": "ram10v2.webp"},
        {"id": 401, "product_id": 76, "path": "ram10v3.webp"},
        
        {"id": 402, "product_id": 77, "path": "mb1v1.webp"},
        {"id": 403, "product_id": 77, "path": "mb1v2.webp"},
        {"id": 404, "product_id": 77, "path": "mb1v3.jpg"},
        {"id": 405, "product_id": 77, "path": "mb1v4.webp"},
        {"id": 406, "product_id": 77, "path": "mb1v5.jpg"},
        {"id": 407, "product_id": 77, "path": "mb1v6.webp"},
        
        {"id": 408, "product_id": 78, "path": "mb2v1.webp"},
        {"id": 409, "product_id": 78, "path": "mb2v2.webp"},
        {"id": 410, "product_id": 78, "path": "mb2v3.webp"},
        {"id": 411, "product_id": 78, "path": "mb2v4.webp"},
        {"id": 412, "product_id": 78, "path": "mb2v5.jpg"},
        {"id": 413, "product_id": 78, "path": "mb2v6.jpg"},
        {"id": 414, "product_id": 78, "path": "mb2v7.webp"},
        
        {"id": 415, "product_id": 79, "path": "mb3v1.webp"},
        {"id": 416, "product_id": 79, "path": "mb3v2.webp"},
        {"id": 417, "product_id": 79, "path": "mb3v3.webp"},
        {"id": 418, "product_id": 79, "path": "mb3v4.jpg"},
        {"id": 419, "product_id": 79, "path": "mb3v5.webp"},
        
        {"id": 420, "product_id": 80, "path": "mb4v1.jpg"},
        {"id": 421, "product_id": 80, "path": "mb4v2.webp"},
        {"id": 422, "product_id": 80, "path": "mb4v3.webp"},
        {"id": 423, "product_id": 80, "path": "mb4v4.webp"},
        {"id": 424, "product_id": 80, "path": "mb4v5.webp"},
        
        {"id": 425, "product_id": 81, "path": "mb5v1.webp"},
        {"id": 426, "product_id": 81, "path": "mb5v2.webp"},
        {"id": 427, "product_id": 81, "path": "mb5v3.webp"},
        {"id": 428, "product_id": 81, "path": "mb5v4.jpg"},
        {"id": 429, "product_id": 81, "path": "mb5v5.webp"},
        {"id": 430, "product_id": 81, "path": "mb5v6.webp"},
        
        {"id": 431, "product_id": 82, "path": "mb6v1.webp"},
        {"id": 432, "product_id": 82, "path": "mb6v2.webp"},
        {"id": 433, "product_id": 82, "path": "mb6v3.webp"},
        {"id": 434, "product_id": 82, "path": "mb6v4.jpg"},
        {"id": 435, "product_id": 82, "path": "mb6v5.jpg"},
        {"id": 436, "product_id": 82, "path": "mb6v6.webp"},
        {"id": 437, "product_id": 82, "path": "mb6v7.webp"},
        
        {"id": 438, "product_id": 83, "path": "mb7v1.webp"},
        {"id": 439, "product_id": 83, "path": "mb7v2.webp"},
        {"id": 440, "product_id": 83, "path": "mb7v3.webp"},
        {"id": 441, "product_id": 83, "path": "mb7v4.webp"},
        {"id": 442, "product_id": 83, "path": "mb7v5.webp"},
        
        {"id": 443, "product_id": 84, "path": "mb8v1.webp"},
        {"id": 444, "product_id": 84, "path": "mb8v2.webp"},
        {"id": 445, "product_id": 84, "path": "mb8v3.webp"},
        {"id": 446, "product_id": 84, "path": "mb8v4.webp"},
        {"id": 447, "product_id": 84, "path": "mb8v5.webp"},
        
        {"id": 448, "product_id": 85, "path": "mb9v1.webp"},
        {"id": 449, "product_id": 85, "path": "mb9v2.webp"},
        {"id": 450, "product_id": 85, "path": "mb9v3.webp"},
        {"id": 451, "product_id": 85, "path": "mb9v4.webp"},
        {"id": 452, "product_id": 85, "path": "mb9v5.webp"},
        
        {"id": 453, "product_id": 86, "path": "mb10v1.webp"},
        {"id": 454, "product_id": 86, "path": "mb10v2.webp"},
        {"id": 455, "product_id": 86, "path": "mb10v3.webp"},
        {"id": 456, "product_id": 86, "path": "mb10v4.webp"},
        {"id": 457, "product_id": 86, "path": "mb10v5.webp"},
        
        {"id": 458, "product_id": 87, "path": "power1v1.webp"},
        {"id": 459, "product_id": 87, "path": "power1v2.webp"},
        {"id": 460, "product_id": 87, "path": "power1v3.webp"},
        {"id": 461, "product_id": 87, "path": "power1v4.webp"},
        {"id": 462, "product_id": 87, "path": "power1v5.webp"},
        
        {"id": 463, "product_id": 88, "path": "power2v1.webp"},
        {"id": 464, "product_id": 88, "path": "power2v2.webp"},
        {"id": 465, "product_id": 88, "path": "power2v3.webp"},
        {"id": 466, "product_id": 88, "path": "power2v4.webp"},
        {"id": 467, "product_id": 88, "path": "power2v5.webp"},
        {"id": 468, "product_id": 88, "path": "power2v6.webp"},
        {"id": 469, "product_id": 88, "path": "power2v7.webp"},
        {"id": 470, "product_id": 88, "path": "power2v8.webp"},
        {"id": 471, "product_id": 88, "path": "power2v9.webp"},
        {"id": 472, "product_id": 88, "path": "power2v11.webp"},
        
        {"id": 473, "product_id": 89, "path": "power3v1.webp"},
        {"id": 474, "product_id": 89, "path": "power3v2.webp"},
        {"id": 475, "product_id": 89, "path": "power3v3.webp"},
        {"id": 476, "product_id": 89, "path": "power3v4.webp"},
        {"id": 477, "product_id": 89, "path": "power3v5.webp"},
        {"id": 478, "product_id": 89, "path": "power3v6.webp"},
        
        {"id": 479, "product_id": 90, "path": "power4v1.webp"},
        {"id": 480, "product_id": 90, "path": "power4v2.webp"},
        {"id": 481, "product_id": 90, "path": "power4v3.webp"},
        {"id": 482, "product_id": 90, "path": "power4v4.webp"},
        {"id": 483, "product_id": 90, "path": "power4v5.webp"},
        {"id": 484, "product_id": 90, "path": "power4v6.webp"},
        {"id": 485, "product_id": 90, "path": "power4v7.webp"},
        
        {"id": 486, "product_id": 91, "path": "power5v1.webp"},
        {"id": 487, "product_id": 91, "path": "power5v2.webp"},
        {"id": 488, "product_id": 91, "path": "power5v3.webp"},
        {"id": 489, "product_id": 91, "path": "power5v4.webp"},
        {"id": 490, "product_id": 91, "path": "power5v5.webp"},
        
        {"id": 491, "product_id": 92, "path": "power6v1.webp"},
        {"id": 492, "product_id": 92, "path": "power6v2.webp"},
        {"id": 493, "product_id": 92, "path": "power6v3.webp"},
        {"id": 494, "product_id": 92, "path": "power6v4.webp"},
        {"id": 495, "product_id": 92, "path": "power6v5.webp"},
        {"id": 496, "product_id": 92, "path": "power6v6.webp"},
        {"id": 497, "product_id": 92, "path": "power6v7.webp"},
        {"id": 498, "product_id": 92, "path": "power6v8.webp"},
        {"id": 499, "product_id": 92, "path": "power6v9.webp"},
        {"id": 500, "product_id": 92, "path": "power6v10.webp"},
        {"id": 501, "product_id": 92, "path": "power6v11.webp"},
        
        {"id": 502, "product_id": 93, "path": "power7v1.webp"},
        {"id": 503, "product_id": 93, "path": "power7v2.webp"},
        {"id": 504, "product_id": 93, "path": "power7v3.webp"},
        {"id": 505, "product_id": 93, "path": "power7v4.webp"},
        {"id": 506, "product_id": 93, "path": "power7v5.webp"},
        {"id": 507, "product_id": 93, "path": "power7v6.webp"},
        
        {"id": 508, "product_id": 94, "path": "power8v1.webp"},
        {"id": 509, "product_id": 94, "path": "power8v2.webp"},
        {"id": 510, "product_id": 94, "path": "power8v3.webp"},
        {"id": 511, "product_id": 94, "path": "power8v4.webp"},
        {"id": 512, "product_id": 94, "path": "power8v5.webp"},
        {"id": 513, "product_id": 94, "path": "power8v6.webp"},
        {"id": 514, "product_id": 94, "path": "power8v7.webp"},
        {"id": 515, "product_id": 94, "path": "power8v8.webp"},
        {"id": 516, "product_id": 94, "path": "power8v9.webp"},
        
        {"id": 517, "product_id": 95, "path": "power9v1.webp"},
        {"id": 518, "product_id": 95, "path": "power9v2.webp"},
        {"id": 519, "product_id": 95, "path": "power9v3.webp"},
        {"id": 520, "product_id": 95, "path": "power9v4.webp"},
        {"id": 521, "product_id": 95, "path": "power9v5.webp"},
        {"id": 522, "product_id": 95, "path": "power9v6.webp"},
        {"id": 523, "product_id": 95, "path": "power9v7.webp"},
        {"id": 524, "product_id": 95, "path": "power9v8.webp"},
        
        {"id": 525, "product_id": 96, "path": "processor1.webp"},
        
        {"id": 526, "product_id": 97, "path": "processor2.webp"},
        
        {"id": 527, "product_id": 98, "path": "processor3.webp"},
        
        {"id": 528, "product_id": 99, "path": "processor4.webp"},
        
        {"id": 529, "product_id": 100, "path": "processor5.webp"},
        
        {"id": 530, "product_id": 101, "path": "processor6.webp"},
        
        {"id": 531, "product_id": 102, "path": "processor7.webp"},
        
        {"id": 532, "product_id": 103, "path": "processor8.webp"},
        
        {"id": 533, "product_id": 104, "path": "processor9.webp"},
        
        {"id": 534, "product_id": 105, "path": "processor10.webp"},
        
        {"id": 535, "product_id": 106, "path": "mouse1v1.webp"},
        {"id": 536, "product_id": 106, "path": "mouse1v2.webp"},
        {"id": 537, "product_id": 106, "path": "mouse1v3.webp"},
        {"id": 538, "product_id": 106, "path": "mouse1v4.webp"},
        {"id": 539, "product_id": 106, "path": "mouse1v5.webp"},
        
        {"id": 540, "product_id": 107, "path": "mouse2v1.webp"},
        {"id": 541, "product_id": 107, "path": "mouse2v2.webp"},
        {"id": 542, "product_id": 107, "path": "mouse2v3.webp"},
        {"id": 543, "product_id": 107, "path": "mouse2v4.webp"},
        {"id": 544, "product_id": 107, "path": "mouse2v5.webp"},
        
        {"id": 545, "product_id": 108, "path": "mouse3v1.webp"},
        {"id": 546, "product_id": 108, "path": "mouse3v2.webp"},
        {"id": 547, "product_id": 108, "path": "mouse3v3.webp"},
        {"id": 548, "product_id": 108, "path": "mouse3v4.webp"},
        {"id": 549, "product_id": 108, "path": "mouse3v5.webp"},
        
        {"id": 550, "product_id": 109, "path": "mouse4v1.webp"},
        {"id": 551, "product_id": 109, "path": "mouse4v2.webp"},
        {"id": 552, "product_id": 109, "path": "mouse4v3.webp"},
        {"id": 553, "product_id": 109, "path": "mouse4v4.webp"},
        {"id": 554, "product_id": 109, "path": "mouse4v5.webp"},
        
        {"id": 555, "product_id": 110, "path": "mouse5v1.webp"},
        {"id": 556, "product_id": 110, "path": "mouse5v2.webp"},
        {"id": 557, "product_id": 110, "path": "mouse5v3.webp"},
        {"id": 558, "product_id": 110, "path": "mouse5v4.webp"},
        {"id": 559, "product_id": 110, "path": "mouse5v5.webp"},
        
        {"id": 560, "product_id": 111, "path": "mouse6v1.webp"},
        {"id": 561, "product_id": 111, "path": "mouse6v2.webp"},
        {"id": 562, "product_id": 111, "path": "mouse6v3.webp"},
        {"id": 563, "product_id": 111, "path": "mouse6v4.webp"},
        {"id": 564, "product_id": 111, "path": "mouse6v5.webp"},
        
        {"id": 565, "product_id": 112, "path": "mouse7v1.webp"},
        {"id": 566, "product_id": 112, "path": "mouse7v2.webp"},
        {"id": 567, "product_id": 112, "path": "mouse7v3.webp"},
        {"id": 568, "product_id": 112, "path": "mouse7v4.webp"},
        {"id": 569, "product_id": 112, "path": "mouse7v5.webp"},
        
        {"id": 570, "product_id": 113, "path": "mouse8v1.webp"},
        {"id": 571, "product_id": 113, "path": "mouse8v2.webp"},
        {"id": 572, "product_id": 113, "path": "mouse8v3.webp"},
        {"id": 573, "product_id": 113, "path": "mouse8v4.webp"},
        {"id": 574, "product_id": 113, "path": "mouse8v5.webp"},
        
        {"id": 575, "product_id": 114, "path": "mouse9v1.webp"},
        {"id": 576, "product_id": 114, "path": "mouse9v2.webp"},
        {"id": 577, "product_id": 114, "path": "mouse9v3.webp"},
        {"id": 578, "product_id": 114, "path": "mouse9v4.webp"},
        {"id": 579, "product_id": 114, "path": "mouse9v5.webp"},
        
        {"id": 580, "product_id": 115, "path": "mouse10v1.webp"},
        {"id": 581, "product_id": 115, "path": "mouse10v2.webp"},
        {"id": 582, "product_id": 115, "path": "mouse10v3.webp"},
        {"id": 583, "product_id": 115, "path": "mouse10v4.webp"},
        {"id": 584, "product_id": 115, "path": "mouse10v5.webp"},

        {"id": 585, "product_id": 116, "path": "keyboard1v1.webp"},
        {"id": 586, "product_id": 116, "path": "keyboard1v2.webp"},
        {"id": 587, "product_id": 116, "path": "keyboard1v3.webp"},
        {"id": 588, "product_id": 116, "path": "keyboard1v4.webp"},
        {"id": 589, "product_id": 116, "path": "keyboard1v5.webp"},

        {"id": 590, "product_id": 117, "path": "keyboard2v1.webp"},
        {"id": 591, "product_id": 117, "path": "keyboard2v2.webp"},
        {"id": 592, "product_id": 117, "path": "keyboard2v3.webp"},
        {"id": 593, "product_id": 117, "path": "keyboard2v4.webp"},
        {"id": 594, "product_id": 117, "path": "keyboard2v5.webp"},

        {"id": 595, "product_id": 118, "path": "keyboard3v1.webp"},
        {"id": 596, "product_id": 118, "path": "keyboard3v2.webp"},
        {"id": 597, "product_id": 118, "path": "keyboard3v3.webp"},
        {"id": 598, "product_id": 118, "path": "keyboard3v4.webp"},
        {"id": 599, "product_id": 118, "path": "keyboard3v5.webp"},

        {"id": 600, "product_id": 119, "path": "keyboard4v1.webp"},
        {"id": 601, "product_id": 119, "path": "keyboard4v2.webp"},
        {"id": 602, "product_id": 119, "path": "keyboard4v3.webp"},
        {"id": 603, "product_id": 119, "path": "keyboard4v4.webp"},
        {"id": 604, "product_id": 119, "path": "keyboard4v5.webp"},

        {"id": 605, "product_id": 120, "path": "keyboard5v1.webp"},
        {"id": 606, "product_id": 120, "path": "keyboard5v2.webp"},
        {"id": 607, "product_id": 120, "path": "keyboard5v3.webp"},
        {"id": 608, "product_id": 120, "path": "keyboard5v4.webp"},
        {"id": 609, "product_id": 120, "path": "keyboard5v5.webp"},

        {"id": 610, "product_id": 121, "path": "keyboard6v1.webp"},
        {"id": 611, "product_id": 121, "path": "keyboard6v2.webp"},
        {"id": 612, "product_id": 121, "path": "keyboard6v3.webp"},
        {"id": 613, "product_id": 121, "path": "keyboard6v4.webp"},
        {"id": 614, "product_id": 121, "path": "keyboard6v5.webp"},

        {"id": 615, "product_id": 122, "path": "keyboard7v1.webp"},
        {"id": 616, "product_id": 122, "path": "keyboard7v2.webp"},
        {"id": 617, "product_id": 122, "path": "keyboard7v3.webp"},
        {"id": 618, "product_id": 122, "path": "keyboard7v4.webp"},
        {"id": 619, "product_id": 122, "path": "keyboard7v5.webp"},

        {"id": 620, "product_id": 123, "path": "keyboard8v1.webp"},
        {"id": 621, "product_id": 123, "path": "keyboard8v2.webp"},
        {"id": 622, "product_id": 123, "path": "keyboard8v3.webp"},
        {"id": 623, "product_id": 123, "path": "keyboard8v4.webp"},
        {"id": 624, "product_id": 123, "path": "keyboard8v5.webp"},

        {"id": 625, "product_id": 124, "path": "keyboard9v1.webp"},
        {"id": 626, "product_id": 124, "path": "keyboard9v2.webp"},
        {"id": 627, "product_id": 124, "path": "keyboard9v3.webp"},
        {"id": 628, "product_id": 124, "path": "keyboard9v4.webp"},
        {"id": 629, "product_id": 124, "path": "keyboard9v5.webp"},

        {"id": 630, "product_id": 125, "path": "keyboard10v1.webp"},
        {"id": 631, "product_id": 125, "path": "keyboard10v2.webp"},
        {"id": 632, "product_id": 125, "path": "keyboard10v3.webp"},
        {"id": 633, "product_id": 125, "path": "keyboard10v4.webp"},
        {"id": 634, "product_id": 125, "path": "keyboard10v5.webp"},

        {"id": 635, "product_id": 126, "path": "monitor1v1.webp"},
        {"id": 636, "product_id": 126, "path": "monitor1v2.webp"},
        {"id": 637, "product_id": 126, "path": "monitor1v3.webp"},
        {"id": 638, "product_id": 126, "path": "monitor1v4.webp"},
        {"id": 639, "product_id": 126, "path": "monitor1v5.webp"},

        {"id": 640, "product_id": 127, "path": "monitor2v1.webp"},
        {"id": 641, "product_id": 127, "path": "monitor2v2.webp"},
        {"id": 642, "product_id": 127, "path": "monitor2v3.webp"},
        {"id": 643, "product_id": 127, "path": "monitor2v4.webp"},
        {"id": 644, "product_id": 127, "path": "monitor2v5.webp"},

        {"id": 645, "product_id": 128, "path": "monitor3v1.webp"},
        {"id": 646, "product_id": 128, "path": "monitor3v2.webp"},
        {"id": 647, "product_id": 128, "path": "monitor3v3.webp"},
        {"id": 648, "product_id": 128, "path": "monitor3v4.webp"},
        {"id": 649, "product_id": 128, "path": "monitor3v5.webp"},

        {"id": 650, "product_id": 129, "path": "monitor4v1.webp"},
        {"id": 651, "product_id": 129, "path": "monitor4v2.webp"},
        {"id": 652, "product_id": 129, "path": "monitor4v3.webp"},
        {"id": 653, "product_id": 129, "path": "monitor4v4.webp"},
        {"id": 654, "product_id": 129, "path": "monitor4v5.webp"},

        {"id": 655, "product_id": 130, "path": "monitor5v1.webp"},
        {"id": 656, "product_id": 130, "path": "monitor5v2.webp"},
        {"id": 657, "product_id": 130, "path": "monitor5v3.webp"},
        {"id": 658, "product_id": 130, "path": "monitor5v4.webp"},
        {"id": 659, "product_id": 130, "path": "monitor5v5.webp"},

        {"id": 660, "product_id": 131, "path": "monitor6v1.webp"},
        {"id": 661, "product_id": 131, "path": "monitor6v2.webp"},
        {"id": 662, "product_id": 131, "path": "monitor6v3.webp"},
        {"id": 663, "product_id": 131, "path": "monitor6v4.webp"},
        {"id": 664, "product_id": 131, "path": "monitor6v5.webp"},

        {"id": 665, "product_id": 132, "path": "monitor7v1.webp"},
        {"id": 666, "product_id": 132, "path": "monitor7v2.webp"},
        {"id": 667, "product_id": 132, "path": "monitor7v3.webp"},
        {"id": 668, "product_id": 132, "path": "monitor7v4.webp"},
        {"id": 669, "product_id": 132, "path": "monitor7v5.webp"},

        {"id": 670, "product_id": 133, "path": "monitor8v1.webp"},
        {"id": 671, "product_id": 133, "path": "monitor8v2.webp"},
        {"id": 672, "product_id": 133, "path": "monitor8v3.webp"},
        {"id": 673, "product_id": 133, "path": "monitor8v4.webp"},
        {"id": 674, "product_id": 133, "path": "monitor8v5.webp"},

        {"id": 675, "product_id": 134, "path": "monitor9v1.webp"},
        {"id": 676, "product_id": 134, "path": "monitor9v2.webp"},
        {"id": 677, "product_id": 134, "path": "monitor9v3.webp"},
        {"id": 678, "product_id": 134, "path": "monitor9v4.webp"},
        {"id": 679, "product_id": 134, "path": "monitor9v5.webp"},

        {"id": 680, "product_id": 135, "path": "monitor10v1.webp"},
        {"id": 681, "product_id": 135, "path": "monitor10v2.webp"},
        {"id": 682, "product_id": 135, "path": "monitor10v3.webp"},
        {"id": 683, "product_id": 135, "path": "monitor10v4.webp"},
        {"id": 684, "product_id": 135, "path": "monitor10v5.webp"},

        {"id": 685, "product_id": 136, "path": "router1v1.webp"},
        {"id": 686, "product_id": 136, "path": "router1v2.webp"},
        {"id": 687, "product_id": 136, "path": "router1v3.webp"},
        {"id": 688, "product_id": 136, "path": "router1v4.webp"},
        {"id": 689, "product_id": 136, "path": "router1v5.webp"},

        {"id": 690, "product_id": 137, "path": "router2v1.webp"},
        {"id": 691, "product_id": 137, "path": "router2v2.webp"},
        {"id": 692, "product_id": 137, "path": "router2v3.webp"},
        {"id": 693, "product_id": 137, "path": "router2v4.webp"},
        {"id": 694, "product_id": 137, "path": "router2v5.webp"},

        {"id": 695, "product_id": 138, "path": "router3v1.webp"},
        {"id": 696, "product_id": 138, "path": "router3v2.webp"},
        {"id": 697, "product_id": 138, "path": "router3v3.webp"},
        {"id": 698, "product_id": 138, "path": "router3v4.webp"},
        {"id": 699, "product_id": 138, "path": "router3v5.webp"},

        {"id": 700, "product_id": 139, "path": "router4v1.jpg"},
        {"id": 701, "product_id": 139, "path": "router4v2.jpg"},
        {"id": 702, "product_id": 139, "path": "router4v3.webp"},
        {"id": 703, "product_id": 139, "path": "router4v4.webp"},
        {"id": 704, "product_id": 139, "path": "router4v5.webp"},

        {"id": 705, "product_id": 140, "path": "router5v1.webp"},
        {"id": 706, "product_id": 140, "path": "router5v2.webp"},
        {"id": 707, "product_id": 140, "path": "router5v3.webp"},
        {"id": 708, "product_id": 140, "path": "router5v4.webp"},
        {"id": 709, "product_id": 140, "path": "router5v5.webp"},

        {"id": 710, "product_id": 141, "path": "router6v1.webp"},
        {"id": 711, "product_id": 141, "path": "router6v2.webp"},
        {"id": 712, "product_id": 141, "path": "router6v3.webp"},
        {"id": 713, "product_id": 141, "path": "router6v4.webp"},
        {"id": 714, "product_id": 141, "path": "router6v5.webp"},

        {"id": 715, "product_id": 142, "path": "router7v1.webp"},
        {"id": 716, "product_id": 142, "path": "router7v2.webp"},
        {"id": 717, "product_id": 142, "path": "router7v3.webp"},
        {"id": 718, "product_id": 142, "path": "router7v4.webp"},
        {"id": 719, "product_id": 142, "path": "router7v5.webp"},

        {"id": 720, "product_id": 143, "path": "router8v1.webp"},
        {"id": 721, "product_id": 143, "path": "router8v2.webp"},
        {"id": 722, "product_id": 143, "path": "router8v3.webp"},
        {"id": 723, "product_id": 143, "path": "router8v4.webp"},
        {"id": 724, "product_id": 143, "path": "router8v5.webp"},

        {"id": 725, "product_id": 144, "path": "router9v1.webp"},
        {"id": 726, "product_id": 144, "path": "router9v2.webp"},
        {"id": 727, "product_id": 144, "path": "router9v3.webp"},
        {"id": 728, "product_id": 144, "path": "router9v4.webp"},
        {"id": 729, "product_id": 144, "path": "router9v5.webp"},

        {"id": 730, "product_id": 145, "path": "router10v1.webp"},
        {"id": 731, "product_id": 145, "path": "router10v2.webp"},
        {"id": 732, "product_id": 145, "path": "router10v3.webp"},
        {"id": 733, "product_id": 145, "path": "router10v4.webp"},
        {"id": 734, "product_id": 145, "path": "router10v5.webp"},

        {"id": 735, "product_id": 146, "path": "cabel1v1.webp"},
        {"id": 736, "product_id": 147, "path": "cabel2v1.webp"},
        {"id": 737, "product_id": 148, "path": "cabel3v1.webp"},
        {"id": 738, "product_id": 149, "path": "cabel4v1.webp"},
        {"id": 739, "product_id": 150, "path": "cabel5v1.webp"},
        {"id": 740, "product_id": 151, "path": "cabel6v1.webp"},
        {"id": 741, "product_id": 152, "path": "cabel7v1.webp"},
        {"id": 742, "product_id": 153, "path": "cabel8v1.webp"},
        {"id": 743, "product_id": 154, "path": "cabel9v1.webp"},
        {"id": 744, "product_id": 155, "path": "cabel10v1.webp"},
    ]

    photo_instances = []
    for photo in tqdm(photo_data, desc="Seeding photos", unit="photo"):
            try:
                product = Product.objects.get(id=photo["product_id"])
                photo_instances.append(
                    PhotoProduct(
                        id=photo["id"],
                        product=product,
                        path=photo["path"]
                    )
                )
                print(Fore.GREEN + f"Successfully added photo ID {photo['id']} for product ID {photo['product_id']}.")
            except Product.DoesNotExist:
                print(Fore.RED + f"Product with ID {photo['product_id']} does not exist. Skipping photo ID {photo['id']}.")
            except Exception as e:
                print(Fore.RED + f"Error adding photo ID {photo['id']}: {e}")

    PhotoProduct.objects.bulk_create(photo_instances)

    print(Fore.GREEN + "Product photos successfully seeded.")

# Seed product categories

def seed_specifications():
    specifications = [
        {"product_id": 1, "parameter_name": "Motherboard", "specification": "MSI PRO B650M-P"},
        {"product_id": 1, "parameter_name": "Case", "specification": "Logic Concept Aramis ARGB black (AT-ARAMIS-10-0000000-0002)"},
        {"product_id": 1, "parameter_name": "Processor", "specification": "AMD Ryzen 5 7500F, 3.7 GHz, 32 MB, OEM (100-000000597)"},
        {"product_id": 1, "parameter_name": "CPU cooling", "specification": "Endorfy Fera 5 (EY3A005)"},
        {"product_id": 1, "parameter_name": "SSD drive", "specification": "Lexar NM620 512GB M.2 2280 PCI-E x4 Gen3 NVMe (LNM620X512G-RNNNG)"},
        {"product_id": 1, "parameter_name": "RAM", "specification": "Kingston Fury Beast, DDR5, 16 GB, 6000MHz, CL36 (KF560C36BBEK2-16)"},
        {"product_id": 1, "parameter_name": "Graphics Card", "specification": "Palit GeForce RTX 4060 TI Dual 8GB GDDR6"},
        {"product_id": 1, "parameter_name": "Charger", "specification": "Thermaltake Litepower II Black 650W (PS-LTP-0650NPCNEU-2)"},
        {"product_id": 1, "parameter_name": "Operating system", "specification": "Windows 10 Home (unactivated) *possibility to purchase licenses by changing attributes"},
        {"product_id": 1, "parameter_name": "The set price includes", "specification": "Assembly of components, BIOS update, Installation of the Operating System, Installation of all updates and drivers, System optimization for better performance"},

        {"product_id": 2, "parameter_name": "Motherboard", "specification": "ASRock B450M PRO4 R2.0"},
        {"product_id": 2, "parameter_name": "Case", "specification": "Endorfy Signum 300 ARGB"},
        {"product_id": 2, "parameter_name": "Processor", "specification": "AMD Ryzen 5 5600"},
        {"product_id": 2, "parameter_name": "CPU cooling", "specification": "BOX (can be changed through additional attributes)"},
        {"product_id": 2, "parameter_name": "SSD drive", "specification": "Lexar NM620 500GB M.2 2280 PCI-E x4 Gen3 NVMe (3300 MB/s | 3000 MB/s) (can be changed through additional attributes)"},
        {"product_id": 2, "parameter_name": "RAM", "specification": "GoodRam/G.skill/Patriot/HyperX/Adata, DDR4, 16 GB (2x8GB), 3200MHz, CL16 (can be changed through additional attributes)"},
        {"product_id": 2, "parameter_name": "Graphics Card", "specification": "PNY GeForce RTX 4060 Ti VERTO Dual Fan 8GB GDDR6"},
        {"product_id": 2, "parameter_name": "Charger", "specification": "Cooler master bronze 550W"},
        {"product_id": 2, "parameter_name": "Operating system", "specification": "Windows 10 Home (unactivated) *possibility to purchase licenses by changing attributes"},
        {"product_id": 2, "parameter_name": "The set price includes", "specification": "Assembly of components, BIOS update, Installation of the Operating System, Installation of all updates and drivers, System optimization for better performance, Door-To-Door 24M warranty"},

        {"product_id": 3, "parameter_name": "Motherboard", "specification": "ASRock Z790 PG LIGHTNING"},
        {"product_id": 3, "parameter_name": "Case", "specification": "Endorfy Arx 500 ARGB (EY2A011)"},
        {"product_id": 3, "parameter_name": "Processor", "specification": "Intel Core i7-14700KF, 3.4 GHz, 33 MB, BOX (BX8071514700KF)"},
        {"product_id": 3, "parameter_name": "CPU cooling", "specification": "Arctic Liquid Freezer III 240 A-RGB Black (ACFRE00142A)"},
        {"product_id": 3, "parameter_name": "SSD drive", "specification": "Lexar NM710 1TB M.2 2280 PCI-E x4 Gen4 NVMe (LNM710X001T-RNNNG)"},
        {"product_id": 3, "parameter_name": "RAM", "specification": "PNY XLR8 Gaming Epic-X, DDR5, 32 GB, 6400MHz, CL40"},
        {"product_id": 3, "parameter_name": "Graphics Card", "specification": "Palit GeForce RTX 4070 Ti SUPER JetStream OC 16GB GDDR6X (NED47TSS19T2-1043J)"},
        {"product_id": 3, "parameter_name": "Charger", "specification": "MSI MAG A750BN PCIE5 750W"},
        {"product_id": 3, "parameter_name": "Operating system", "specification": "Windows 10 Home (unactivated) *possibility to purchase licenses by changing attributes"},
        {"product_id": 3, "parameter_name": "The set price includes", "specification": "Assembly of components, BIOS update, Installation of the Operating System, Installation of all updates and drivers, System optimization for better performance"},
    
        {"product_id": 4, "parameter_name": "Motherboard", "specification": "ASRock B450M PRO4 R2.0"},
        {"product_id": 4, "parameter_name": "Case", "specification": "Logic Aramis ARGB White"},
        {"product_id": 4, "parameter_name": "Processor", "specification": "AMD Ryzen 7 5700X"},
        {"product_id": 4, "parameter_name": "CPU cooling", "specification": "BOX**can be changed through additional attributes"},
        {"product_id": 4, "parameter_name": "SSD drive", "specification": "Lexar NM620 500GB M.2 2280 PCI-E x4 Gen3 NVMe (3300 MB/s |3000 MB/s)*can be changed through additional attributes"},
        {"product_id": 4, "parameter_name": "RAM", "specification": "GoodRam/G.skill/Patriot/HyperX/Adata, DDR4, 16 GB (2x8GB), 3200MHz, CL16**can be changed through additional attributes"},
        {"product_id": 4, "parameter_name": "Graphics Card", "specification": "Inno3D GeForce RTX 4060 Twin X2 8GB GDDR6X DLSS 3"},
        {"product_id": 4, "parameter_name": "Charger", "specification": "Cooler master bronze 550W"},
        {"product_id": 4, "parameter_name": "Operating system", "specification": "Windows 10 Home (unactivated)**possibility to purchase licenses by changing attributes"},
        {"product_id": 4, "parameter_name": "The set price includes", "specification": "Assembly of components BIOS update Installation of the Operating System Installation of all updates and drivers System optimization for better performance Door-To-Door 24M warranty"},
        
        {"product_id": 5, "parameter_name": "Motherboard", "specification": "Gigabyte B760M DS3H"},
        {"product_id": 5, "parameter_name": "Case", "specification": "MSI MAG FORGE 112R ARGB Tempered Glass"},
        {"product_id": 5, "parameter_name": "Processor", "specification": "Intel Core I5-14400F"},
        {"product_id": 5, "parameter_name": "CPU cooling", "specification": "BOX"},
        {"product_id": 5, "parameter_name": "SSD drive", "specification": "Lexar NM620 512GB"},
        {"product_id": 5, "parameter_name": "RAM", "specification": "GoodRam/G.skill/Patriot/HyperX/Adata, DDR4, 16 GB (2x8GB), 3600MHz, CL18"},
        {"product_id": 5, "parameter_name": "Graphics Card", "specification": "ASROCK RADEON RX 7800 XT CHALLENGER 16G GDDR6"},
        {"product_id": 5, "parameter_name": "Charger", "specification": "MSI MAG A650BN 650W 80Plus Bronze power supply"},
        {"product_id": 5, "parameter_name": "Operating system", "specification": "Windows 10 Home (unactivated) *possibility to purchase licenses by changing attributes"},
        {"product_id": 5, "parameter_name": "The set price includes", "specification": "Assembly of components, BIOS update, Installation of the Operating System, Installation of all updates and drivers, System optimization for better performance"},
        
        {"product_id": 6, "parameter_name": "Motherboard", "specification": "ASRock B760M PG RIPTIDE DDR5"},
        {"product_id": 6, "parameter_name": "Case", "specification": "ARX 500 ARGB Endorfs"},
        {"product_id": 6, "parameter_name": "Processor", "specification": "Intel Core i5-14600KF"},
        {"product_id": 6, "parameter_name": "CPU cooling", "specification": "Fortis 5 Endorfs"},
        {"product_id": 6, "parameter_name": "SSD drive", "specification": "Lexar NM620 512GB"},
        {"product_id": 6, "parameter_name": "RAM", "specification": "Kingston DDR5 Fury Beast Black 16GB (2x8GB)/6000 CL40"},
        {"product_id": 6, "parameter_name": "Graphics Card", "specification": "ASRock Radeon RX 7900 GRE Challenger 16GB"},
        {"product_id": 6, "parameter_name": "Charger", "specification": "Endorfy L5 700W"},
        {"product_id": 6, "parameter_name": "Operating system", "specification": "Windows 10 Home (unactivated)"},
        {"product_id": 6, "parameter_name": "The set price includes", "specification": "Installation of components, BIOS update, Installation of the operating system, Installation of all updates and drivers, Optimization of the system for better performance"},

        {"product_id": 7, "parameter_name": "Motherboard", "specification": "Asrock B650M PRO RS"},
        {"product_id": 7, "parameter_name": "Case", "specification": "MSI MAG FORGE 112R ARGB Tempered Glass"},
        {"product_id": 7, "parameter_name": "Processor", "specification": "AMD Ryzen 5 7600"},
        {"product_id": 7, "parameter_name": "CPU cooling", "specification": "BOX"},
        {"product_id": 7, "parameter_name": "SSD drive", "specification": "Lexar NM620 500GB"},
        {"product_id": 7, "parameter_name": "RAM", "specification": "Kingston/Patriot/Goodram/G.Skill/PNY/Adata 16GB (2x8GB) 6000MHz DDR5"},
        {"product_id": 7, "parameter_name": "Graphics Card", "specification": "ASROCK RADEON RX 7800 XT CHALLENGER 16G GDDR6"},
        {"product_id": 7, "parameter_name": "Charger", "specification": "Endorfy L5 700W"},
        {"product_id": 7, "parameter_name": "Operating system", "specification": "Windows 10 Home (unactivated)"},
        {"product_id": 7, "parameter_name": "The set price includes", "specification": "Assembly of components, BIOS update, Installation of the Operating System, Installation of all updates and drivers, System optimization for better performance"},
        
        {"product_id": 8, "parameter_name": "Motherboard", "specification": "ASRock B650M PRO RS"},
        {"product_id": 8, "parameter_name": "Case", "specification": "Endorfy Regnum 400 ARGB (EY2A009)"},
        {"product_id": 8, "parameter_name": "Processor", "specification": "Ryzen 7 7800X3D"},
        {"product_id": 8, "parameter_name": "CPU cooling", "specification": "AiO MSI MAG CoreLiquid M240 240mm"},
        {"product_id": 8, "parameter_name": "SSD drive", "specification": "Lexar Professional NM800 Pro 512GB M.2 2280 PCI-E x4 Gen4 NVMe"},
        {"product_id": 8, "parameter_name": "RAM", "specification": "Kingston Fury Beast, DDR5, 16 GB, 5600MHz, CL40 (KF556C40BBK2-16)"},
        {"product_id": 8, "parameter_name": "Graphics Card", "specification": "ASRock Radeon RX 7900 XTX Phantom Gaming 24GB GDDR6"},
        {"product_id": 8, "parameter_name": "Charger", "specification": "Endorfy FM5 1000W"},
        {"product_id": 8, "parameter_name": "Operating system", "specification": "Windows 10 Home (unactivated)**possibility to purchase licenses by changing attributes"},
        {"product_id": 8, "parameter_name": "The set price includes", "specification": "Assembly of components, BIOS update, Installation of the Operating System, Installation of all updates and drivers, System optimization for better performance"},
        
        {"product_id": 9, "parameter_name": "Processor", "specification": "Intel Core i7-13700F (16 cores, 24 threads, 2.10-5.20 GHz, 30 MB cache)"},
        {"product_id": 9, "parameter_name": "Chipset", "specification": "Intel B760"},
        {"product_id": 9, "parameter_name": "RAM", "specification": "32 GB (DIMM DDR5, 6000MHz)"},
        {"product_id": 9, "parameter_name": "Memory architecture", "specification": "Dual-channel"},
        {"product_id": 9, "parameter_name": "Maximum amount of RAM supported", "specification": "192GB"},
        {"product_id": 9, "parameter_name": "Number of memory slots (total/free)", "specification": "4/2"},
        {"product_id": 9, "parameter_name": "RAM voltage", "specification": "1.35 V"},
        {"product_id": 9, "parameter_name": "Graphics Card", "specification": "NVIDIA GeForce RTX 4060 Ti"},
        {"product_id": 9, "parameter_name": "Graphics card memory size", "specification": "8192 MB GDDR6 (own memory)"},
        {"product_id": 9, "parameter_name": "PCIe 4.0 SSD", "specification": "1000 GB SSD M.2 PCIe 4.0"},
        {"product_id": 9, "parameter_name": "Height", "specification": "454mm"},
        {"product_id": 9, "parameter_name": "Width", "specification": "215mm"},
        {"product_id": 9, "parameter_name": "Depth", "specification": "474mm"},
        {"product_id": 9, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 9, "parameter_name": "Type of warranty", "specification": "x-kom G4M3R (door-to-door)"},
        {"product_id": 9, "parameter_name": "Producer code", "specification": "GHi7F13D5406T-S-A-11H"},

        {"product_id": 10, "parameter_name": "Processor", "specification": "Apple M2 (8 cores, ARM)"},
        {"product_id": 10, "parameter_name": "RAM", "specification": "16 GB (unified memory)"},
        {"product_id": 10, "parameter_name": "Maximum amount of RAM supported", "specification": "16GB"},
        {"product_id": 10, "parameter_name": "Number of memory slots (total/free)", "specification": "0/0 (soldered memory)"},
        {"product_id": 10, "parameter_name": "PCIe SSDs (soldered)", "specification": "256GB"},
        {"product_id": 10, "parameter_name": "Touchscreen", "specification": "NO"},
        {"product_id": 10, "parameter_name": "Screen type", "specification": "Glossy, LED, IPS, Liquid Retina"},
        {"product_id": 10, "parameter_name": "Screen diagonal", "specification": "13.6\""},
        {"product_id": 10, "parameter_name": "Screen resolution", "specification": "2560x1664"},
        {"product_id": 10, "parameter_name": "Matrix brightness", "specification": "500 cd/m²"},
        {"product_id": 10, "parameter_name": "Graphics Card", "specification": "Apple M2 [8 cores]"},
        {"product_id": 10, "parameter_name": "Graphics card memory", "specification": "Shared memory"},
        {"product_id": 10, "parameter_name": "Sound", "specification": "Built-in four speakersThree built-in microphones"},
        {"product_id": 10, "parameter_name": "Webcam", "specification": "FaceTime HDFull HD"},
        {"product_id": 10, "parameter_name": "Communication", "specification": "WiFi 6Bluetooth 5.0 module"},
        {"product_id": 10, "parameter_name": "Connectors", "specification": "USB Type-C (with Thunderbolt™ 4) - 2 pcs.Headphone output/microphone input - 1 pc.MagSafe 3 - 1 pc."},
        {"product_id": 10, "parameter_name": "Battery type", "specification": "Lithium polymer"},
        {"product_id": 10, "parameter_name": "Dominant color", "specification": "Navy"},
        {"product_id": 10, "parameter_name": "Fingerprint reader", "specification": "Yes"},
        {"product_id": 10, "parameter_name": "Sensors", "specification": "Light sensor"},
        {"product_id": 10, "parameter_name": "Backlit keyboard", "specification": "YesKeyboard backlight color: White"},
        {"product_id": 10, "parameter_name": "Security", "specification": "TPM encryptionTouch ID reader"},
        {"product_id": 10, "parameter_name": "Housing and workmanship", "specification": "Aluminum matrix coverAluminum laptop interiorAluminum housing"},
        {"product_id": 10, "parameter_name": "Operating system", "specification": "macOS Monterey"},
        {"product_id": 10, "parameter_name": "Software included", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 10, "parameter_name": "Charger", "specification": "30 WPlug: Magsafe 3"},
        {"product_id": 10, "parameter_name": "Additional information", "specification": "Force Touch multi-touch trackpadMatrix with 100% DCI-P3 color coverageYear of release: 2022"},
        {"product_id": 10, "parameter_name": "Height", "specification": "11.3mm"},
        {"product_id": 10, "parameter_name": "Width", "specification": "304mm"},
        {"product_id": 10, "parameter_name": "Depth", "specification": "215mm"},
        {"product_id": 10, "parameter_name": "Weight", "specification": "1.24 kg"},
        {"product_id": 10, "parameter_name": "Accessories included", "specification": "ChargerUSB Type-C -> MagSafe cable"},
        {"product_id": 10, "parameter_name": "Type of warranty", "specification": "Standard"},
        {"product_id": 10, "parameter_name": "Guarantee", "specification": "12 months (manufacturers warranty)"},
        {"product_id": 10, "parameter_name": "Manufacturer code", "specification": "MLY33ZE/A/R1 - CTO [Z160000DB]"},
        
        {"product_id": 11, "parameter_name": "Processor", "specification": "AMD Ryzen™ 5 5625U (6 cores, 12 threads, 2.30–4.30 GHz, 19 MB cache)"},
        {"product_id": 11, "parameter_name": "RAM", "specification": "16GB (DDR4, 3200MHz)"},
        {"product_id": 11, "parameter_name": "Maximum amount of RAM supported", "specification": "64GB"},
        {"product_id": 11, "parameter_name": "Number of memory slots (total/free)", "specification": "2/0"},
        {"product_id": 11, "parameter_name": "M.2 PCIe SSD", "specification": "512GB"},
        {"product_id": 11, "parameter_name": "Touchscreen", "specification": "NO"},
        {"product_id": 11, "parameter_name": "Screen type", "specification": "Matte, LED, IPS"},
        {"product_id": 11, "parameter_name": "Screen diagonal", "specification": "15.6\""},
        {"product_id": 11, "parameter_name": "Screen resolution", "specification": "1920 x 1080 (Full HD)"},
        {"product_id": 11, "parameter_name": "Matrix brightness", "specification": "250 cd/m²"},
        {"product_id": 11, "parameter_name": "Graphics Card", "specification": "AMD Radeon™ Graphics"},
        {"product_id": 11, "parameter_name": "Graphics card memory", "specification": "Shared memory"},
        {"product_id": 11, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in microphone"},
        {"product_id": 11, "parameter_name": "Webcam", "specification": "H.D"},
        {"product_id": 11, "parameter_name": "Communication", "specification": "WiFi 5Bluetooth 5.0 module"},
        {"product_id": 11, "parameter_name": "Connectors", "specification": "USB 3.2 Gen. 1 - 2 pcs.USB Type-C - 1 pc.HDMI 1.4b - 1 pc.SD memory card reader - 1 pc.RJ-45 (LAN) - 1 pc.Headphone output/microphone input - 1 pc.DC-in (power input) - 1 pc."},
        {"product_id": 11, "parameter_name": "Battery type", "specification": "Lithium polymer"},
        {"product_id": 11, "parameter_name": "Dominant color", "specification": "Silver"},
        {"product_id": 11, "parameter_name": "Fingerprint reader", "specification": "NO"},
        {"product_id": 11, "parameter_name": "Backlit keyboard", "specification": "YesKeyboard backlight color: White"},
        {"product_id": 11, "parameter_name": "Security", "specification": "TPM encryption"},
        {"product_id": 11, "parameter_name": "Operating system", "specification": "Microsoft Windows 11 Home"},
        {"product_id": 11, "parameter_name": "Software included", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 11, "parameter_name": "Charger", "specification": "45 W"},
        {"product_id": 11, "parameter_name": "Additional information", "specification": "Separate numeric keyboardMulti-touch, intuitive touchpad"},
        {"product_id": 11, "parameter_name": "Height", "specification": "19.9mm"},
        {"product_id": 11, "parameter_name": "Width", "specification": "358 mm"},
        {"product_id": 11, "parameter_name": "Depth", "specification": "242 mm"},
        {"product_id": 11, "parameter_name": "Weight", "specification": "1.74 kg"},
        {"product_id": 11, "parameter_name": "Accessories included", "specification": "ChargerCorporate laptop bag"},
        {"product_id": 11, "parameter_name": "Type of warranty", "specification": "On-site 36 months"},
        {"product_id": 11, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 11, "parameter_name": "Manufacturer code", "specification": "8A646EA"},
        
        {"product_id": 12, "parameter_name": "Processor", "specification": "Intel® Core™ i5-12450H (8 cores, 12 threads, 3.30-4.40 GHz, 12MB cache)"},
        {"product_id": 12, "parameter_name": "RAM", "specification": "16GB (DDR4, 3200MHz)"},
        {"product_id": 12, "parameter_name": "Maximum amount of RAM supported", "specification": "64GB"},
        {"product_id": 12, "parameter_name": "Number of memory slots (total/free)", "specification": "2/0"},
        {"product_id": 12, "parameter_name": "M.2 PCIe SSD", "specification": "512 GB"},
        {"product_id": 12, "parameter_name": "Options for adding disks", "specification": "Possibility to install a SATA drive (mounting elements included)"},
        {"product_id": 12, "parameter_name": "Touchscreen", "specification": "NO"},
        {"product_id": 12, "parameter_name": "Screen type", "specification": "Matte, LED, IPS"},
        {"product_id": 12, "parameter_name": "Screen diagonal", "specification": "15.6\""},
        {"product_id": 12, "parameter_name": "Screen resolution", "specification": "1920 x 1080 (Full HD)"},
        {"product_id": 12, "parameter_name": "Screen refresh rate", "specification": "144Hz"},
        {"product_id": 12, "parameter_name": "Graphics Card", "specification": "NVIDIA GeForce RTX 2050"},
        {"product_id": 12, "parameter_name": "Graphics card memory", "specification": "4GB GDDR6"},
        {"product_id": 12, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in microphone"},
        {"product_id": 12, "parameter_name": "Webcam", "specification": "HD"},
        {"product_id": 12, "parameter_name": "Communication", "specification": "LAN 1GbpsWiFi 6Bluetooth 5.2 module"},
        {"product_id": 12, "parameter_name": "Connectors", "specification": "USB 3.2 Gen. 1 - 3 pcs.USB Type-C (with DisplayPort) - 1 pc.HDMI - 1 pc.RJ-45 (LAN) - 1 pc.Microphone input - 1 pc.Headphone/speaker output - 1 pc.DC-in (power input) - 1 pc."},
        {"product_id": 12, "parameter_name": "Battery type", "specification": "Lithium polymer"},
        {"product_id": 12, "parameter_name": "Battery capacity", "specification": "3-chamber, 4600 mAh"},
        {"product_id": 12, "parameter_name": "Dominant color", "specification": "Black"},
        {"product_id": 12, "parameter_name": "Fingerprint reader", "specification": "NO"},
        {"product_id": 12, "parameter_name": "Backlit keyboard", "specification": "YesKeyboard backlight color: Red"},
        {"product_id": 12, "parameter_name": "Security", "specification": "Can be secured with a cable (Kensington Lock port)TPM encryption"},
        {"product_id": 12, "parameter_name": "Operating system", "specification": "No system"},
        {"product_id": 12, "parameter_name": "Charger", "specification": "120 W"},
        {"product_id": 12, "parameter_name": "Additional information", "specification": "Multi-touch, intuitive touchpad"},
        {"product_id": 12, "parameter_name": "Height", "specification": "21.7mm"},
        {"product_id": 12, "parameter_name": "Width", "specification": "359 mm"},
        {"product_id": 12, "parameter_name": "Depth", "specification": "254mm"},
        {"product_id": 12, "parameter_name": "Weight", "specification": "1.86 kg"},
        {"product_id": 12, "parameter_name": "Accessories included", "specification": "Charger"},
        {"product_id": 12, "parameter_name": "Type of warranty", "specification": "Standard"},
        {"product_id": 12, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        
        {"product_id": 13, "parameter_name": "Processor", "specification": "Intel® Core™ i5-1235U (10 cores, 12 threads, 3.30-4.40 GHz, 12MB cache)"},
        {"product_id": 13, "parameter_name": "RAM", "specification": "16GB (DDR4, 3200MHz)"},
        {"product_id": 13, "parameter_name": "Maximum amount of RAM supported", "specification": "16GB"},
        {"product_id": 13, "parameter_name": "Number of memory slots (total/free)", "specification": "1/0"},
        {"product_id": 13, "parameter_name": "M.2 PCIe SSD", "specification": "512 GB"},
        {"product_id": 13, "parameter_name": "Touchscreen", "specification": "NO"},
        {"product_id": 13, "parameter_name": "Screen type", "specification": "Matte, LED, IPS"},
        {"product_id": 13, "parameter_name": "Screen diagonal", "specification": "15.6\""},
        {"product_id": 13, "parameter_name": "Screen resolution", "specification": "1920 x 1080 (Full HD)"},
        {"product_id": 13, "parameter_name": "Matrix brightness", "specification": "250 cd/m²"},
        {"product_id": 13, "parameter_name": "Graphics Card", "specification": "Intel Iris Xe Graphics"},
        {"product_id": 13, "parameter_name": "Graphics card memory", "specification": "Shared memory"},
        {"product_id": 13, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in microphone"},
        {"product_id": 13, "parameter_name": "Webcam", "specification": "HD"},
        {"product_id": 13, "parameter_name": "Communication", "specification": "Wi-Fi 6EBluetooth 5.3 module"},
        {"product_id": 13, "parameter_name": "Connectors", "specification": "USB 2.0 - 1 pc.USB 3.2 Gen. 1 - 2 pcs.USB Type-C - 1 pc.HDMI - 1 pc.DC-in (power input) - 1 pc."},
        {"product_id": 13, "parameter_name": "Battery type", "specification": "Lithium-ion"},
        {"product_id": 13, "parameter_name": "Dominant color", "specification": "Blue"},
        {"product_id": 13, "parameter_name": "Fingerprint reader", "specification": "Yes"},
        {"product_id": 13, "parameter_name": "Security", "specification": "TPM encryptionCamera with built-in cover"},
        {"product_id": 13, "parameter_name": "Housing and workmanship", "specification": "Military standard MIL-STD-810H"},
        {"product_id": 13, "parameter_name": "Operating system", "specification": "Microsoft Windows 11 Home"},
        {"product_id": 13, "parameter_name": "Software included", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 13, "parameter_name": "Charger", "specification": "May 192.37 A45 W"},
        {"product_id": 13, "parameter_name": "Additional information", "specification": "Separate numeric keyboard"},
        {"product_id": 13, "parameter_name": "Height", "specification": "17.9mm"},
        {"product_id": 13, "parameter_name": "Width", "specification": "360mm"},
        {"product_id": 13, "parameter_name": "Depth", "specification": "233mm"},
        {"product_id": 13, "parameter_name": "Weight", "specification": "1.70kg"},
        {"product_id": 13, "parameter_name": "Accessories included", "specification": "Charger"},
        {"product_id": 13, "parameter_name": "Type of warranty", "specification": "Standard"},
        {"product_id": 13, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},

        {"product_id": 14, "parameter_name": "Processor", "specification": "Intel® Core™ i5-1235U (10 cores, 12 threads, 3.30-4.40 GHz, 12MB cache)"},
        {"product_id": 14, "parameter_name": "RAM", "specification": "16GB (DDR4, 2666MHz)"},
        {"product_id": 14, "parameter_name": "Maximum amount of RAM supported", "specification": "32GB"},
        {"product_id": 14, "parameter_name": "Number of memory slots (total/free)", "specification": "2/0"},
        {"product_id": 14, "parameter_name": "M.2 PCIe SSD", "specification": "1000 GB"},
        {"product_id": 14, "parameter_name": "Touchscreen", "specification": "NO"},
        {"product_id": 14, "parameter_name": "Screen type", "specification": "Matte, LED, WVA"},
        {"product_id": 14, "parameter_name": "Screen diagonal", "specification": "15.6\""},
        {"product_id": 14, "parameter_name": "Screen resolution", "specification": "1920 x 1080 (Full HD)"},
        {"product_id": 14, "parameter_name": "Screen refresh rate", "specification": "120 Hz"},
        {"product_id": 14, "parameter_name": "Matrix brightness", "specification": "250 cd/m²"},
        {"product_id": 14, "parameter_name": "Graphics Card", "specification": "Intel Iris Xe Graphics"},
        {"product_id": 14, "parameter_name": "Graphics card memory", "specification": "Shared memory"},
        {"product_id": 14, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in microphone"},
        {"product_id": 14, "parameter_name": "Webcam", "specification": "HD"},
        {"product_id": 14, "parameter_name": "Communication", "specification": "WiFi 6Bluetooth 5.2 module"},
        {"product_id": 14, "parameter_name": "Connectors", "specification": "USB 2.0 - 1 pc.USB 3.2 Gen. 1 - 2 pcs.HDMI 1.4 - 1 pc.SD memory card reader - 1 pc.Headphone output/microphone input - 1 pc.DC-in (power input) - 1 pc."},
        {"product_id": 14, "parameter_name": "Battery type", "specification": "Lithium-ion"},
        {"product_id": 14, "parameter_name": "Battery capacity", "specification": "3-cell, 3467 mAh"},
        {"product_id": 14, "parameter_name": "Dominant color", "specification": "Black"},
        {"product_id": 14, "parameter_name": "Fingerprint reader", "specification": "NO"},
        {"product_id": 14, "parameter_name": "Backlit keyboard", "specification": "NO"},
        {"product_id": 14, "parameter_name": "Security", "specification": "TPM encryption"},
        {"product_id": 14, "parameter_name": "Operating system", "specification": "Microsoft Windows 11 Home"},
        {"product_id": 14, "parameter_name": "Software included", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 14, "parameter_name": "Charger", "specification": "19.5V 3.34 A 65 WPlug: round with pin - 4.5-3.0 mmLA65NS2-01"},
        {"product_id": 14, "parameter_name": "Additional information", "specification": "Separate numeric keyboardMulti-touch, intuitive touchpad"},
        {"product_id": 14, "parameter_name": "Height", "specification": "19mm"},
        {"product_id": 14, "parameter_name": "Width", "specification": "359 mm"},
        {"product_id": 14, "parameter_name": "Depth", "specification": "235mm"},
        {"product_id": 14, "parameter_name": "Weight", "specification": "1.67 kg"},
        {"product_id": 14, "parameter_name": "Accessories included", "specification": "Charger"},
        {"product_id": 14, "parameter_name": "Type of warranty", "specification": "Next Business Day 36 months"},
        {"product_id": 14, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 14, "parameter_name": "Manufacturer code", "specification": "Inspiron-3520-9874"},

        {"product_id": 15, "parameter_name": "Processor", "specification": "Intel® Core™ i5-1235U (10 cores, 12 threads, 3.30-4.40 GHz, 12MB cache)"},
        {"product_id": 15, "parameter_name": "RAM", "specification": "16GB (DDR4, 2666MHz)"},
        {"product_id": 15, "parameter_name": "Maximum amount of RAM supported", "specification": "32GB"},
        {"product_id": 15, "parameter_name": "Number of memory slots (total/free)", "specification": "2/0"},
        {"product_id": 15, "parameter_name": "M.2 PCIe SSD", "specification": "1000 GB"},
        {"product_id": 15, "parameter_name": "Touchscreen", "specification": "NO"},
        {"product_id": 15, "parameter_name": "Screen type", "specification": "Matte, LED, WVA"},
        {"product_id": 15, "parameter_name": "Screen diagonal", "specification": "15.6\""},
        {"product_id": 15, "parameter_name": "Screen resolution", "specification": "1920 x 1080 (Full HD)"},
        {"product_id": 15, "parameter_name": "Screen refresh rate", "specification": "120 Hz"},
        {"product_id": 15, "parameter_name": "Matrix brightness", "specification": "250 cd/m²"},
        {"product_id": 15, "parameter_name": "Graphics Card", "specification": "Intel Iris Xe Graphics"},
        {"product_id": 15, "parameter_name": "Graphics card memory", "specification": "Shared memory"},
        {"product_id": 15, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in microphone"},
        {"product_id": 15, "parameter_name": "Webcam", "specification": "HD"},
        {"product_id": 15, "parameter_name": "Communication", "specification": "WiFi 6Bluetooth 5.2 module"},
        {"product_id": 15, "parameter_name": "Connectors", "specification": "USB 2.0 - 1 pc.USB 3.2 Gen. 1 - 2 pcs.HDMI 1.4 - 1 pc.SD memory card reader - 1 pc.Headphone output/microphone input - 1 pc.DC-in (power input) - 1 pc."},
        {"product_id": 15, "parameter_name": "Battery type", "specification": "Lithium-ion"},
        {"product_id": 15, "parameter_name": "Battery capacity", "specification": "3-cell, 3467 mAh"},
        {"product_id": 15, "parameter_name": "Dominant color", "specification": "Silver"},
        {"product_id": 15, "parameter_name": "Fingerprint reader", "specification": "NO"},
        {"product_id": 15, "parameter_name": "Backlit keyboard", "specification": "NO"},
        {"product_id": 15, "parameter_name": "Security", "specification": "TPM encryption"},
        {"product_id": 15, "parameter_name": "Operating system", "specification": "Microsoft Windows 11 Home"},
        {"product_id": 15, "parameter_name": "Software included", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 15, "parameter_name": "Charger", "specification": "19.5V 3.34 A 65 WPlug: round with pin - 4.5-3.0 mmLA65NS2-01"},
        {"product_id": 15, "parameter_name": "Additional information", "specification": "Separate numeric keyboardMulti-touch, intuitive touchpad"},
        {"product_id": 15, "parameter_name": "Height", "specification": "19mm"},
        {"product_id": 15, "parameter_name": "Width", "specification": "359 mm"},
        {"product_id": 15, "parameter_name": "Depth", "specification": "235mm"},
        {"product_id": 15, "parameter_name": "Weight", "specification": "1.67 kg"},
        {"product_id": 15, "parameter_name": "Accessories included", "specification": "Charger"},
        {"product_id": 15, "parameter_name": "Type of warranty", "specification": "Next Business Day 36 months"},
        {"product_id": 15, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 15, "parameter_name": "Manufacturer code", "specification": "Inspiron-3520-9973"},

        {"product_id": 16, "parameter_name": "Processor", "specification": "Intel® Celeron N4500 (2 cores, 2 threads, 1.10-2.80 GHz, 4 MB cache)"},
        {"product_id": 16, "parameter_name": "RAM", "specification": "8GB (LPDDR4x, 2133MHz)"},
        {"product_id": 16, "parameter_name": "Maximum amount of RAM supported", "specification": "8GB"},
        {"product_id": 16, "parameter_name": "Number of memory slots (total/free)", "specification": "0/0 (soldered memory)"},
        {"product_id": 16, "parameter_name": "eMMC disk", "specification": "128 GB"},
        {"product_id": 16, "parameter_name": "Touchscreen", "specification": "NO"},
        {"product_id": 16, "parameter_name": "Screen type", "specification": "Matte, LED, IPS"},
        {"product_id": 16, "parameter_name": "Screen diagonal", "specification": "15.6\""},
        {"product_id": 16, "parameter_name": "Screen resolution", "specification": "1920 x 1080 (Full HD)"},
        {"product_id": 16, "parameter_name": "Graphics Card", "specification": "Intel UHD Graphics"},
        {"product_id": 16, "parameter_name": "Graphics card memory", "specification": "Shared memory"},
        {"product_id": 16, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in two microphones"},
        {"product_id": 16, "parameter_name": "Webcam", "specification": "H.D"},
        {"product_id": 16, "parameter_name": "Communication", "specification": "WiFi 6Bluetooth 5.0 module"},
        {"product_id": 16, "parameter_name": "Connectors", "specification": "USB 3.2 Gen. 1 - 2 pcs.USB Type-C (with DisplayPort) - 1 pc.USB Type-C (with DisplayPort and Power Delivery) - 1 pc.MicroSD memory card reader - 1 pc.Headphone output/microphone input - 1 pc."},
        {"product_id": 16, "parameter_name": "Battery type", "specification": "Lithium-ion"},
        {"product_id": 16, "parameter_name": "Dominant color", "specification": "Silver"},
        {"product_id": 16, "parameter_name": "Fingerprint reader", "specification": "NO"},
        {"product_id": 16, "parameter_name": "Backlit keyboard", "specification": "NO"},
        {"product_id": 16, "parameter_name": "Security", "specification": "Can be secured with a cable (Kensington Lock port)TPM encryption"},
        {"product_id": 16, "parameter_name": "Operating system", "specification": "ChromeOS"},
        {"product_id": 16, "parameter_name": "Software included", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 16, "parameter_name": "Charger", "specification": "45 WPlug: USB-C"},
        {"product_id": 16, "parameter_name": "Additional information", "specification": "Separate numeric keyboardMulti-touch, intuitive touchpad"},
        {"product_id": 16, "parameter_name": "Height", "specification": "20mm"},
        {"product_id": 16, "parameter_name": "Width", "specification": "366 mm"},
        {"product_id": 16, "parameter_name": "Depth", "specification": "244 mm"},
        {"product_id": 16, "parameter_name": "Weight", "specification": "1.60 kg"},
        {"product_id": 16, "parameter_name": "Accessories included", "specification": "Charger"},
        {"product_id": 16, "parameter_name": "Type of warranty", "specification": "Standard"},
        {"product_id": 16, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 16, "parameter_name": "Manufacturer code", "specification": "CB315-4H-C567 || NX.KB9EP.001"},
        
        {"product_id": 17, "parameter_name": "Processor", "specification": "Intel® Core™ i5-1240P (12 cores, 16 threads, 3.30-4.40 GHz, 12MB cache)"},
        {"product_id": 17, "parameter_name": "RAM", "specification": "16GB (LPDDR5, 4800MHz)"},
        {"product_id": 17, "parameter_name": "Maximum amount of RAM supported", "specification": "16GB"},
        {"product_id": 17, "parameter_name": "Number of memory slots (total/free)", "specification": "0/0 (soldered memory)"},
        {"product_id": 17, "parameter_name": "M.2 PCIe SSD", "specification": "512 GB"},
        {"product_id": 17, "parameter_name": "Touchscreen", "specification": "NO"},
        {"product_id": 17, "parameter_name": "Screen type", "specification": "Glossy, OLED"},
        {"product_id": 17, "parameter_name": "Screen diagonal", "specification": "14.0\""},
        {"product_id": 17, "parameter_name": "Screen resolution", "specification": "1920 x 1200 (WUXGA)"},
        {"product_id": 17, "parameter_name": "Matrix brightness", "specification": "400 cd/m²"},
        {"product_id": 17, "parameter_name": "Graphics Card", "specification": "Intel Iris Xe Graphics"},
        {"product_id": 17, "parameter_name": "Graphics card memory", "specification": "Shared memory"},
        {"product_id": 17, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in microphone"},
        {"product_id": 17, "parameter_name": "Webcam", "specification": "Infrared cameraToF cameraFull HD"},
        {"product_id": 17, "parameter_name": "Communication", "specification": "Wi-Fi 6EBluetooth 5.1 module"},
        {"product_id": 17, "parameter_name": "Connectors", "specification": "USB 3.2 Gen. 1 - 1 pc.USB Type-C (with Thunderbolt™ 4) - 2 pcs.HDMI 2.1 - 1 pc.Headphone output/microphone input - 1 pc."},
        {"product_id": 17, "parameter_name": "Dominant color", "specification": "Gray"},
        {"product_id": 17, "parameter_name": "Fingerprint reader", "specification": "NO"},
        {"product_id": 17, "parameter_name": "Backlit keyboard", "specification": "YesKeyboard backlight color: White"},
        {"product_id": 17, "parameter_name": "Security", "specification": "TPM encryptionWindows HelloCamera with built-in cover"},
        {"product_id": 17, "parameter_name": "Housing and workmanship", "specification": "Aluminum matrix coverAluminum laptop interiorAluminum housingMilitary standard MIL-STD-810H"},
        {"product_id": 17, "parameter_name": "Operating system", "specification": "Microsoft Windows 11 Home"},
        {"product_id": 17, "parameter_name": "Software included", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 17, "parameter_name": "Charger", "specification": "65 WPlug: USB-C"},
        {"product_id": 17, "parameter_name": "Additional information", "specification": "Multi-touch, intuitive touchpadMatrix with 100% DCI-P3 color coverageHDR 500"},
        {"product_id": 17, "parameter_name": "Height", "specification": "14.9mm"},
        {"product_id": 17, "parameter_name": "Width", "specification": "312mm"},
        {"product_id": 17, "parameter_name": "Depth", "specification": "221 mm"},
        {"product_id": 17, "parameter_name": "Weight", "specification": "1.35kg"},
        {"product_id": 17, "parameter_name": "Accessories included", "specification": "Charger"},
        {"product_id": 17, "parameter_name": "Type of warranty", "specification": "Standard"},
        {"product_id": 17, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 17, "parameter_name": "Manufacturer code", "specification": "82WU009DPB"},
        
        {"product_id": 18, "parameter_name": "Processor", "specification": "Intel® Core™ i7-11370H (4 cores, 8 threads, 3.30-4.80 GHz, 12MB cache)"},
        {"product_id": 18, "parameter_name": "RAM", "specification": "32 GB (DDR4, 2666 MHz)"},
        {"product_id": 18, "parameter_name": "Maximum amount of RAM supported", "specification": "32 GB"},
        {"product_id": 18, "parameter_name": "Number of memory slots (total/free)", "specification": "0/0 (soldered memory)"},
        {"product_id": 18, "parameter_name": "M.2 PCIe SSD", "specification": "2000 GB"},
        {"product_id": 18, "parameter_name": "Touchscreen", "specification": "Yes"},
        {"product_id": 18, "parameter_name": "Screen type", "specification": "Glossy, LED"},
        {"product_id": 18, "parameter_name": "Screen diagonal", "specification": "14.4\""},
        {"product_id": 18, "parameter_name": "Screen resolution", "specification": "2400 x 1600"},
        {"product_id": 18, "parameter_name": "Screen refresh rate", "specification": "120 Hz"},
        {"product_id": 18, "parameter_name": "Graphics Card", "specification": "NVIDIA GeForce RTX 3050 TiIntel Iris Xe Graphics"},
        {"product_id": 18, "parameter_name": "Graphics card memory", "specification": "4GB GDDR6"},
        {"product_id": 18, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in microphone"},
        {"product_id": 18, "parameter_name": "Webcam", "specification": "Full HD"},
        {"product_id": 18, "parameter_name": "Communication", "specification": "Wi-Fi 6Bluetooth 5.1 module"},
        {"product_id": 18, "parameter_name": "Connectors", "specification": "USB Type-C (with Thunderbolt™ 4) - 2 pcsOutput headphone/microphone input - 1 pc.Surface Connect - 1 pc."},
        {"product_id": 18, "parameter_name": "Battery type", "specification": "Lithium-Ion"},
        {"product_id": 18, "parameter_name": "Battery capacity", "specification": "6-cell, 5099 mAh"},
        {"product_id": 18, "parameter_name": "Dominant color", "specification": "Platinum"},
        {"product_id": 18, "parameter_name": "Fingerprint reader", "specification": "No"},
        {"product_id": 18, "parameter_name": "Sensors", "specification": "AccelerometerMagnetometerLight sensorGyroscope"},
        {"product_id": 18, "parameter_name": "Backlit keyboard", "specification": "YesKeyboard backlight color: White"},
        {"product_id": 18, "parameter_name": "Security", "specification": "TPM encryptionCasing and design: Magnesium-aluminum housing"},
        {"product_id": 18, "parameter_name": "Operating System", "specification": "Microsoft Windows 11 Home"},
        {"product_id": 18, "parameter_name": "Included software", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 18, "parameter_name": "Width", "specification": "323 mm"},
        {"product_id": 18, "parameter_name": "Depth", "specification": "228 mm"},
        {"product_id": 18, "parameter_name": "Weight", "specification": "1.82 kg"},
        {"product_id": 18, "parameter_name": "Included accessories", "specification": "Power Supply"},
        {"product_id": 18, "parameter_name": "Warranty type", "specification": "Standard"},
        {"product_id": 18, "parameter_name": "Warranty", "specification": "12 months (manufacturers warranty)"},
        {"product_id": 18, "parameter_name": "Manufacturer code", "specification": "AI2-00009"},

        {"product_id": 19, "parameter_name": "Processor", "specification": "Intel® Core™ i7-13700H (14 cores, 20 threads, 3.70-5.00 GHz, 24 MB cache)"},
        {"product_id": 19, "parameter_name": "RAM", "specification": "32 GB (LPDDR5x, 5200 MHz)"},
        {"product_id": 19, "parameter_name": "Maximum amount of RAM supported", "specification": "16GB"},
        {"product_id": 19, "parameter_name": "Number of memory slots (total/free)", "specification": "0/0 (soldered memory)"},
        {"product_id": 19, "parameter_name": "M.2 PCIe SSD", "specification": "1024GB"},
        {"product_id": 19, "parameter_name": "Touchscreen", "specification": "Yes"},
        {"product_id": 19, "parameter_name": "Screen type", "specification": "Glossy, LED"},
        {"product_id": 19, "parameter_name": "Screen diagonal", "specification": "14.4\""},
        {"product_id": 19, "parameter_name": "Screen resolution", "specification": "2400x1600"},
        {"product_id": 19, "parameter_name": "Screen refresh rate", "specification": "120 Hz"},
        {"product_id": 19, "parameter_name": "Graphics Card", "specification": "NVIDIA GeForce RTX 4050Intel Iris Xe Graphics"},
        {"product_id": 19, "parameter_name": "Graphics card memory", "specification": "6GB GDDR6"},
        {"product_id": 19, "parameter_name": "Sound", "specification": "Built-in stereo speakersBuilt-in microphone"},
        {"product_id": 19, "parameter_name": "Webcam", "specification": "Full HD"},
        {"product_id": 19, "parameter_name": "Communication", "specification": "Wi-Fi 6EBluetooth 5.3 module"},
        {"product_id": 19, "parameter_name": "Connectors", "specification": "USB 3.2 Gen. 1 - 1 pc.USB Type-C (with Thunderbolt™ 4) - 2 pcs.Headphone output/microphone input - 1 pc.Surface Connect - 1 pc."},
        {"product_id": 19, "parameter_name": "Battery type", "specification": "Lithium-ion"},
        {"product_id": 19, "parameter_name": "Dominant color", "specification": "Platinum"},
        {"product_id": 19, "parameter_name": "Fingerprint reader", "specification": "NO"},
        {"product_id": 19, "parameter_name": "Sensors", "specification": "AccelerometerGyroscope"},
        {"product_id": 19, "parameter_name": "Backlit keyboard", "specification": "YesKeyboard backlight color: White"},
        {"product_id": 19, "parameter_name": "Security", "specification": "TPM encryption"},
        {"product_id": 19, "parameter_name": "Housing and workmanship", "specification": "Aluminum housing"},
        {"product_id": 19, "parameter_name": "Operating system", "specification": "Microsoft Windows 11 Home"},
        {"product_id": 19, "parameter_name": "Software included", "specification": "Recovery partition (option to restore the system from disk)"},
        {"product_id": 19, "parameter_name": "Additional information", "specification": "Multi-touch, intuitive touchpad"},
        {"product_id": 19, "parameter_name": "Height", "specification": "22mm"},
        {"product_id": 19, "parameter_name": "Width", "specification": "323mm"},
        {"product_id": 19, "parameter_name": "Depth", "specification": "230mm"},
        {"product_id": 19, "parameter_name": "Weight", "specification": "1.98 kg"},
        {"product_id": 19, "parameter_name": "Accessories included", "specification": "Charger"},
        {"product_id": 19, "parameter_name": "Type of warranty", "specification": "Standard"},
        {"product_id": 19, "parameter_name": "Guarantee", "specification": "12 months (manufacturers warranty)"},
        {"product_id": 19, "parameter_name": "Producent code", "specification": "Z1I-00009"},
        
        {"product_id": 20, "parameter_name": "Enclosure type", "specification": "Middle Tower"},
        {"product_id": 20, "parameter_name": "Sidebar", "specification": "Tempered glass"},
        {"product_id": 20, "parameter_name": "Highlight", "specification": "RGB"},
        {"product_id": 20, "parameter_name": "Motherboard standard", "specification": "ATX, microATX, Mini-ITX"},
        {"product_id": 20, "parameter_name": "Power supply standard", "specification": "ATX"},
        {"product_id": 20, "parameter_name": "Space for internal disks/drives", "specification": "2x 2.5\", 2x 3.5\""},
        {"product_id": 20, "parameter_name": "Slots for expansion cards", "specification": "7"},
        {"product_id": 20, "parameter_name": "Maximum graphics card length", "specification": "330 mm"},
        {"product_id": 20, "parameter_name": "Maximum CPU cooling height", "specification": "161 mm"},
        {"product_id": 20, "parameter_name": "Maximum number of fans", "specification": "8"},
        {"product_id": 20, "parameter_name": "Fan mounting options", "specification": "3x 120/140 mm (front), 1x 120 mm (rear), 2x 120 mm (top)"},
        {"product_id": 20, "parameter_name": "Water cooling installation options", "specification": "1x 120 mm (front) - radiator, 1x 140 mm (front) - radiator, 1x 240 mm (front) - radiator, 1x 280 mm (front) - radiator, 1x 360 mm (front) - radiator, 1x 120 mm (rear) - radiator, 1x 120 mm (top) - radiator, 1x 240 mm (top) - radiator, 1x 140 mm (top) - radiator"},
        {"product_id": 20, "parameter_name": "Number of fans installed", "specification": "4"},
        {"product_id": 20, "parameter_name": "Fans installed", "specification": "3x 120 mm (front), 1x 120 mm (rear)"},
        {"product_id": 20, "parameter_name": "Buttons and controls", "specification": "Power, Reset"},
        {"product_id": 20, "parameter_name": "Derived connectors", "specification": "USB 2.0 - 1 pc, USB 3.2 Gen. 1 - 2 pcs, HD Audio (CTIA – SPK/Mic)"},
        {"product_id": 20, "parameter_name": "Material", "specification": "Steel, Tempered glass, ABS"},
        {"product_id": 20, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 20, "parameter_name": "Additional information", "specification": "Mounting the power supply at the bottom of the case, Dust filters"},
        {"product_id": 20, "parameter_name": "Included accessories", "specification": "Set of screws and mounting elements"},
        {"product_id": 20, "parameter_name": "Height", "specification": "448 mm"},
        {"product_id": 20, "parameter_name": "Width", "specification": "204 mm"},
        {"product_id": 20, "parameter_name": "Depth", "specification": "386 mm"},
        {"product_id": 20, "parameter_name": "Weight", "specification": "4.6 kg"},
        {"product_id": 20, "parameter_name": "Warranty", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 20, "parameter_name": "Manufacturer code", "specification": "NFO-2154"},
        
        {"product_id": 21, "parameter_name": "Housing type", "specification": "Midi Tower"},
        {"product_id": 21, "parameter_name": "Motherboard standard", "specification": "Mini-ITX, Micro-ATX, ATX"},
        {"product_id": 21, "parameter_name": "Compatible power supply standard", "specification": "ATX"},
        {"product_id": 21, "parameter_name": "Power supply location", "specification": "Hole"},
        {"product_id": 21, "parameter_name": "Maximum length of the power supply", "specification": "170mm"},
        {"product_id": 21, "parameter_name": "Maximum CPU cooling height", "specification": "161mm"},
        {"product_id": 21, "parameter_name": "Maximum length of the GPU graphics card", "specification": "330mm"},
        {"product_id": 21, "parameter_name": "I/O panel", "specification": "USB 3.0 Type-A x2, USB 2.0 Type-A x1, Mini Jack x2"},
        {"product_id": 21, "parameter_name": "Side panel type", "specification": "Tempered glass"},
        {"product_id": 21, "parameter_name": "Type of front panel", "specification": "Mesh (dense mesh)"},
        {"product_id": 21, "parameter_name": "Number of fans installed", "specification": "4"},
        {"product_id": 21, "parameter_name": "Fans installed", "specification": "4x 120 mm"},
        {"product_id": 21, "parameter_name": "Maximum number of fans", "specification": "8"},
        {"product_id": 21, "parameter_name": "Possibility of mounting fans - bottom", "specification": "2x 120 mm"},
        {"product_id": 21, "parameter_name": "Possibility of mounting fans - top", "specification": "2x 120 mm, 1x 140 mm"},
        {"product_id": 21, "parameter_name": "Possibility to install fans - front", "specification": "3x 140 mm, 3x 120 mm"},
        {"product_id": 21, "parameter_name": "Possibility of mounting fans - rear", "specification": "1x 120 mm"},
        {"product_id": 21, "parameter_name": "Fan speed +/-10%", "specification": "1200 RPM"},
        {"product_id": 21, "parameter_name": "Fan life", "specification": "40000"},
        {"product_id": 21, "parameter_name": "Fan airflow", "specification": "36.5 CFM"},
        {"product_id": 21, "parameter_name": "Fan noise level", "specification": "21.2 dB"},
        {"product_id": 21, "parameter_name": "Possibility to install water cooling (AIO)", "specification": "Yes"},
        {"product_id": 21, "parameter_name": "Possibility to install liquid cooling - top", "specification": "240mm, 120mm"},
        {"product_id": 21, "parameter_name": "Possibility to install liquid cooling - front", "specification": "360mm, 280mm, 240mm, 140mm, 120mm"},
        {"product_id": 21, "parameter_name": "Possibility to install liquid cooling - rear", "specification": "120mm"},
        {"product_id": 21, "parameter_name": "Number of expansion slots", "specification": "7"},
        {"product_id": 21, "parameter_name": "Number of places for 2.5\" drives (SSD/HDD)", "specification": "2"},
        {"product_id": 21, "parameter_name": "Number of places for 3.5\" drives (SSD/HDD)", "specification": "2"},
        {"product_id": 21, "parameter_name": "Power supply compartment", "specification": "Yes"},
        {"product_id": 21, "parameter_name": "Power supply included", "specification": "NO"},
        {"product_id": 21, "parameter_name": "Security", "specification": "Dust filters"},
        {"product_id": 21, "parameter_name": "Material", "specification": "Tempered glass, Steel, ABS"},
        {"product_id": 21, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 21, "parameter_name": "Length", "specification": "386mm"},
        {"product_id": 21, "parameter_name": "Width", "specification": "204mm"},
        {"product_id": 21, "parameter_name": "Height", "specification": "448mm"},
        {"product_id": 21, "parameter_name": "Libra", "specification": "4.3kg"},
        {"product_id": 21, "parameter_name": "Accessories included", "specification": "Set of mounting elements, assembly instructions"},

        {"product_id": 22, "parameter_name": "Housing type", "specification": "Middle Tower"},
        {"product_id": 22, "parameter_name": "Side panel", "specification": "Tempered glass"},
        {"product_id": 22, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 22, "parameter_name": "Motherboard standard", "specification": "ATX"},
        {"product_id": 22, "parameter_name": "Power supply standard", "specification": "ATX"},
        {"product_id": 22, "parameter_name": "Space for internal disks/drives", "specification": "4 x 2.5\", 1 x 3.5\"/2.5\", 1 x 3.5\""},
        {"product_id": 22, "parameter_name": "Slots for expansion cards", "specification": "7 + 3 vertically"},
        {"product_id": 22, "parameter_name": "Maximum length of the graphics card", "specification": "345mm"},
        {"product_id": 22, "parameter_name": "Maximum CPU cooling height", "specification": "180mm"},
        {"product_id": 22, "parameter_name": "Maximum number of fans", "specification": "8"},
        {"product_id": 22, "parameter_name": "Fan mounting options", "specification": "2x 120 mm or 2x 140 mm (top), 2x 120 mm (power supply tunnel)"},
        {"product_id": 22, "parameter_name": "Water cooling installation options", "specification": "1 x 280 mm (front) - radiator, 1 x 360 mm (front) - radiator, 1 x 120 mm (rear) - radiator, 1 x 140 mm (rear) - radiator, 1 x 240 mm (top) - radiator, 1 x 280 mm (top) - radiator"},
        {"product_id": 22, "parameter_name": "Number of fans installed", "specification": "4"},
        {"product_id": 22, "parameter_name": "Fans installed", "specification": "3x 140 mm (front) - ARGB backlight, 1x 140 mm (rear) - ARGB backlight"},
        {"product_id": 22, "parameter_name": "Buttons and controls", "specification": "Power, Reset, ARGB controller"},
        {"product_id": 22, "parameter_name": "Lead-out connectors", "specification": "USB 3.2 Gen. 1 - 2 pcs., USB 3.2 Gen. 1 Type-C - 1 pc., Headphone/speaker output - 2 pcs."},
        {"product_id": 22, "parameter_name": "Material", "specification": "Steel"},
        {"product_id": 22, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 22, "parameter_name": "Additional information", "specification": "Cable management system, A hole supporting the installation of a processor cooler, Mounting the power supply at the bottom of the housing, Dust filters, Removable HDD cage, Side panel in the form of a door, Possibility to install water cooling"},
        {"product_id": 22, "parameter_name": "Height", "specification": "488mm"},
        {"product_id": 22, "parameter_name": "Width", "specification": "220mm"},
        {"product_id": 22, "parameter_name": "Depth", "specification": "408mm"},
        {"product_id": 22, "parameter_name": "Weight", "specification": "6.4kg"},
        {"product_id": 22, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 22, "parameter_name": "Manufacturer code", "specification": "AT-SIROCO-MG-10-00ARGB-0002"},
        
        {"product_id": 23, "parameter_name": "Dimensions", "specification": "239 x 528 x 477 mm"},
        {"product_id": 23, "parameter_name": "Material", "specification": "Steel, tempered glass"},
        {"product_id": 23, "parameter_name": "Standard", "specification": "Micro-ATX, Mini-ITX, ATX, E-ATX"},
        {"product_id": 23, "parameter_name": "Possibility to install fans", "specification": "3x 120 mm (side panel), 3x 120 mm (Top), 1x 120 mm (Basement), 1x 120 mm (Rear)"},
        {"product_id": 23, "parameter_name": "Possibility to install liquid cooling", "specification": "1x max. 360 mm (side panel), 1x max. 360 mm (top), 1x max. 120 mm (rear)"},
        {"product_id": 23, "parameter_name": "Sinuses", "specification": "3x 3.5\" or 4x 2.5\""},
        {"product_id": 23, "parameter_name": "Charger", "specification": "1x ATX (max 230mm length)"},
        {"product_id": 23, "parameter_name": "The amount of space for expansion cards", "specification": "7"},
        {"product_id": 23, "parameter_name": "I/O-Panel", "specification": "1x Power, 2x USB 3.0 (Type-A, USB 3.2 Gen 1, max. 5 Gbit/s), 1x USB 3.1 (Type C, USB 3.2 Gen 2, max. 10 Gbit/s), 1x 3.5-mm-Combo-Audio, 1x ARGB Mode, 1x ARGB Color"},
        {"product_id": 23, "parameter_name": "Maximum GPU length", "specification": "440mm"},
        {"product_id": 23, "parameter_name": "Maximum CPU cooling height", "specification": "180mm"},
        {"product_id": 23, "parameter_name": "Included", "specification": "Case, GPU Holder, ARGB controller, Optional flap with disk holder, Accessory box"},

        {"product_id": 24, "parameter_name": "Case type", "specification": "Middle Tower"},
        {"product_id": 24, "parameter_name": "Side panel", "specification": "Tempered glass"},
        {"product_id": 24, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 24, "parameter_name": "Backlight fans", "specification": "No information"},
        {"product_id": 24, "parameter_name": "Motherboard standard", "specification": "ATX, microATX, Mini-ITX"},
        {"product_id": 24, "parameter_name": "PSU standard", "specification": "ATX"},
        {"product_id": 24, "parameter_name": "Internal disk/drive slots", "specification": "4 x 2.5\", 1 x 3.5\"/2.5\", 1 x 3.5\""},
        {"product_id": 24, "parameter_name": "Expansion card slots", "specification": "7"},
        {"product_id": 24, "parameter_name": "Maximum graphics card length", "specification": "340 mm"},
        {"product_id": 24, "parameter_name": "Maximum CPU cooler height", "specification": "155 mm"},
        {"product_id": 24, "parameter_name": "Maximum number of fans", "specification": "6"},
        {"product_id": 24, "parameter_name": "Fan Mounting Options", "specification": "3x 120/140 mm (front), 1x 120 mm (back), 2x 120/140 mm (top)"},
        {"product_id": 24, "parameter_name": "Number of Installed Fans", "specification": "4"},
        {"product_id": 24, "parameter_name": "Installed Fans", "specification": "3x 120 mm (front) - ARGB lighting, 1x 120 mm (back) - ARGB lighting"},
        {"product_id": 24, "parameter_name": "Buttons and Controls", "specification": "Power, Reset"},
        {"product_id": 24, "parameter_name": "Connectors", "specification": "USB 2.0 - 2 pcs., USB 3.2 Gen. 1 - 1 pc., Headphone/speaker output - 1 pc."},
        {"product_id": 24, "parameter_name": "Material", "specification": "Plastic, Steel, Glass"},
        {"product_id": 24, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 24, "parameter_name": "Additional information", "specification": "Cable arrangement system, Opening to support CPU cooler assembly, Power supply unit mounted at the bottom of the case, Anti-dust filters, Side panel in the form of a door"},
        {"product_id": 24, "parameter_name": "Accessories included", "specification": "Set of screws and mounting elements"},
        {"product_id": 24, "parameter_name": "Height", "specification": "450 mm"},
        {"product_id": 24, "parameter_name": "Width", "specification": "200 mm"},
        {"product_id": 24, "parameter_name": "Depth", "specification": "390 mm"},
        {"product_id": 24, "parameter_name": "Warranty", "specification": "24 months (manufacturer's warranty)"},
        {"product_id": 24, "parameter_name": "Manufacturer's code", "specification": "AT-PORTOS-10-0000000-0002"},

        {"product_id": 25, "parameter_name": "Housing type", "specification": "Middle Tower"},
        {"product_id": 25, "parameter_name": "Side panel", "specification": "Tempered glass"},
        {"product_id": 25, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 25, "parameter_name": "Illuminated fans", "specification": "Yes"},
        {"product_id": 25, "parameter_name": "Motherboard standard", "specification": "ATX, microATX, Mini-ITX"},
        {"product_id": 25, "parameter_name": "Power supply standard", "specification": "ATX"},
        {"product_id": 25, "parameter_name": "Space for internal disks/drives", "specification": "2 x 2.5\", 2 x 3.5\"/2.5\""},
        {"product_id": 25, "parameter_name": "Slots for expansion cards", "specification": "7"},
        {"product_id": 25, "parameter_name": "Maximum length of the graphics card", "specification": "350mm"},
        {"product_id": 25, "parameter_name": "Maximum CPU cooling height", "specification": "160mm"},
        {"product_id": 25, "parameter_name": "Maximum number of fans", "specification": "5"},
        {"product_id": 25, "parameter_name": "Fan mounting options", "specification": "2x 120/140 mm (front), 1x 120 mm (rear), 2x 120/140 mm (top)"},
        {"product_id": 25, "parameter_name": "Water cooling installation options", "specification": "1 x 120 mm (front) - radiator, 1 x 140 mm (front) - radiator, 1 x 200 mm (front) - radiator, 1 x 240 mm (front) - radiator, 1 x 280 mm (front) - radiator, 1 x 92 mm (top) - radiator, 1 x 120 mm (top) - radiator, 1 x 140 mm (top) - radiator, 1 x 240 mm (top) - radiator, 1 x 280 mm (top) - radiator"},
        {"product_id": 25, "parameter_name": "Number of fans installed", "specification": "3"},
        {"product_id": 25, "parameter_name": "Fans installed", "specification": "2x 140 mm (front) - ARGB backlight, 1x 120 mm (rear) - ARGB backlight"},
        {"product_id": 25, "parameter_name": "Buttons and controls", "specification": "Power"},
        {"product_id": 25, "parameter_name": "Lead-out connectors", "specification": "USB 3.2 Gen. 1 - 2 pcs., USB 3.2 Gen. 1 Type-C - 1 pc., Headphone/speaker output - 1 pc., Microphone input - 1 pc."},
        {"product_id": 25, "parameter_name": "Material", "specification": "Steel, Tempered glass"},
        {"product_id": 25, "parameter_name": "Color", "specification": "White"},
        {"product_id": 25, "parameter_name": "Additional information", "specification": "Cable management system, A hole supporting the installation of a processor cooler, Mounting the power supply at the bottom of the housing, Dust filters, Fan controller/hub, Possibility to install water cooling"},
        {"product_id": 25, "parameter_name": "Height", "specification": "485mm"},
        {"product_id": 25, "parameter_name": "Width", "specification": "205mm"},
        {"product_id": 25, "parameter_name": "Depth", "specification": "415mm"},
        {"product_id": 25, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 25, "parameter_name": "Manufacturer code", "specification": "GELI-912"},

        {"product_id": 26, "parameter_name": "Housing type", "specification": "Middle Tower"},
        {"product_id": 26, "parameter_name": "Side panel", "specification": "Tempered glass"},
        {"product_id": 26, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 26, "parameter_name": "Illuminated fans", "specification": "Yes"},
        {"product_id": 26, "parameter_name": "Motherboard standard", "specification": "ATX, m-ATX, Mini-ITX"},
        {"product_id": 26, "parameter_name": "Power supply standard", "specification": "ATX"},
        {"product_id": 26, "parameter_name": "Space for internal disks/drives", "specification": "4 x 2.5\", 1 x 3.5\"/2.5\", 1 x 3.5\""},
        {"product_id": 26, "parameter_name": "Slots for expansion cards", "specification": "7"},
        {"product_id": 26, "parameter_name": "Maximum length of the graphics card", "specification": "340mm"},
        {"product_id": 26, "parameter_name": "Maximum CPU cooling height", "specification": "155mm"},
        {"product_id": 26, "parameter_name": "Maximum number of fans", "specification": "8"},
        {"product_id": 26, "parameter_name": "Fan mounting options", "specification": "3x 120 mm or 2x 140 mm (front), 1x 120 mm (rear), 2x 120/140 mm (top), 2x 120/140 mm (bottom)"},
        {"product_id": 26, "parameter_name": "Number of fans installed", "specification": "4"},
        {"product_id": 26, "parameter_name": "Fans installed", "specification": "3x 120 mm (front) - ARGB backlight, 1x 120 mm (rear) - ARGB backlight"},
        {"product_id": 26, "parameter_name": "Buttons and controls", "specification": "Power, Reset"},
        {"product_id": 26, "parameter_name": "Lead-out connectors", "specification": "USB 2.0 - 2 pcs., USB 3.2 Gen. 1 - 1 pc., Headphone/speaker output - 1 pc."},
        {"product_id": 26, "parameter_name": "Material", "specification": "Plastic, steel, Glass"},
        {"product_id": 26, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 26, "parameter_name": "Additional information", "specification": "Cable management system, A hole supporting the installation of a processor cooler, Mounting the power supply at the bottom of the housing, Dust filters, Side panel in the form of a door"},
        {"product_id": 26, "parameter_name": "Height", "specification": "450mm"},
        {"product_id": 26, "parameter_name": "Width", "specification": "200mm"},
        {"product_id": 26, "parameter_name": "Depth", "specification": "390mm"},
        {"product_id": 26, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 26, "parameter_name": "Manufacturer code", "specification": "AT-ARAMIS-10-0000000-0002"},

        {"product_id": 27, "parameter_name": "Housing type", "specification": "Mini Tower"},
        {"product_id": 27, "parameter_name": "Side panel", "specification": "Tempered glass"},
        {"product_id": 27, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 27, "parameter_name": "Motherboard standard", "specification": "m-ATX, Mini-ITX"},
        {"product_id": 27, "parameter_name": "Power supply standard", "specification": "ATX"},
        {"product_id": 27, "parameter_name": "Space for internal disks/drives", "specification": "1 x 2.5\", 1 x 3.5\"/2.5\", 1 x 3.5\""},
        {"product_id": 27, "parameter_name": "Slots for expansion cards", "specification": "4"},
        {"product_id": 27, "parameter_name": "Maximum length of the graphics card", "specification": "290mm"},
        {"product_id": 27, "parameter_name": "Maximum CPU cooling height", "specification": "160mm"},
        {"product_id": 27, "parameter_name": "Maximum number of fans", "specification": "3"},
        {"product_id": 27, "parameter_name": "Fan mounting options", "specification": "2x 120/140 mm (front), 1x 120 mm (rear)"},
        {"product_id": 27, "parameter_name": "Number of fans installed", "specification": "3"},
        {"product_id": 27, "parameter_name": "Fans installed", "specification": "2x 120 mm (front) - ARGB backlight, 1x 120 mm (rear) - ARGB backlight"},
        {"product_id": 27, "parameter_name": "Buttons and controls", "specification": "Power, Reset"},
        {"product_id": 27, "parameter_name": "Lead-out connectors", "specification": "USB 2.0 - 2 pcs., USB 3.2 Gen. 1 - 1 pc., Headphone/speaker output - 1 pc., Microphone input - 1 pc."},
        {"product_id": 27, "parameter_name": "Material", "specification": "Plastic, steel, Glass"},
        {"product_id": 27, "parameter_name": "Color", "specification": "White"},
        {"product_id": 27, "parameter_name": "Additional information", "specification": "Cable management system, A hole supporting the installation of a processor cooler, Mounting the power supply at the bottom of the housing, Dust filters"},
        {"product_id": 27, "parameter_name": "Height", "specification": "385mm"},
        {"product_id": 27, "parameter_name": "Width", "specification": "200mm"},
        {"product_id": 27, "parameter_name": "Depth", "specification": "340mm"},
        {"product_id": 27, "parameter_name": "Weight", "specification": "3.6kg"},
        {"product_id": 27, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 27, "parameter_name": "Manufacturer code", "specification": "AM-ARAMIS-20-0000000-0002"},
    
        {"product_id": 28, "parameter_name": "Product type", "specification": "PC case"},
        {"product_id": 28, "parameter_name": "Color", "specification": "black"},
        {"product_id": 28, "parameter_name": "Dimensions (height × width × depth)", "specification": "486×228×429mm"},
        {"product_id": 28, "parameter_name": "Motherboard standard", "specification": "ATX, microATX, ITX"},
        {"product_id": 28, "parameter_name": "Maximum graphics card (GPU) length", "specification": "350mm"},
        {"product_id": 28, "parameter_name": "Maximum height of the processor cooling system", "specification": "179mm"},
        {"product_id": 28, "parameter_name": "Maximum power supply unit (PSU) length", "specification": "300mm"},
        {"product_id": 28, "parameter_name": "Slots for expansion cards", "specification": "7"},
        {"product_id": 28, "parameter_name": "Number of bays", "specification": "1× 2.5”/3.5”, 6× 2.5″"},
        {"product_id": 28, "parameter_name": "Number of fans (maximum)", "specification": "7"},
        {"product_id": 28, "parameter_name": "Number of fans (included)", "specification": "4"},
        {"product_id": 28, "parameter_name": "Front", "specification": "3× Stratus 140 PWM fan (200–1200 rpm)"},
        {"product_id": 28, "parameter_name": "Back", "specification": "1× Stratus 140 PWM fan (200–1200 rpm)"},
        {"product_id": 28, "parameter_name": "Compatibility with liquid cooling radiators", "specification": "Front 1× 120, 240, 280, 360 mmTop 1× 120, 240, 280  mmRear 1× 120, 140 mm"},
        {"product_id": 28, "parameter_name": "Dust filters", "specification": "Front, Top, Bottom"},
        {"product_id": 28, "parameter_name": "I/O panel", "specification": "1× USB-C2× USB-A1× headphones (3.5 mm  minijack)1× microphone (3.5 mm minijack)1× POWER  button1× RESET/LED button"},
        
        {"product_id": 29, "parameter_name": "Number of fans", "specification": "2 pcs"},
        {"product_id": 29, "parameter_name": "Fan dimensions", "specification": "140 mm"},
        {"product_id": 29, "parameter_name": "Speed control", "specification": "PWM control"},
        {"product_id": 29, "parameter_name": "Minimum fan speed", "specification": "800 rpm"},
        {"product_id": 29, "parameter_name": "Maximum fan speed", "specification": "2000 rpm"},
        {"product_id": 29, "parameter_name": "Heatsink Material", "specification": "Aluminum + Copper"},
        {"product_id": 29, "parameter_name": "Radiator dimensions", "specification": "317 x 138 x 38 mm"},
        {"product_id": 29, "parameter_name": "Backlight", "specification": "None"},
        {"product_id": 29, "parameter_name": "Outer diameter of hoses", "specification": "12.4 mm"},
        {"product_id": 29, "parameter_name": "Inner diameter of hoses", "specification": "6 mm"},
        {"product_id": 29, "parameter_name": "Hose length", "specification": "450 mm"},
        {"product_id": 29, "parameter_name": "Power consumption", "specification": "2.7 W"},
        {"product_id": 29, "parameter_name": "Weight", "specification": "1572 g"},
        {"product_id": 29, "parameter_name": "Airflow", "specification": "72.8 CFM"},
        {"product_id": 29, "parameter_name": "Compatibility", "specification": "Intel LGA 1700, 115X, 2011-3, 2066, AMD AM4"},
        {"product_id": 29, "parameter_name": "Block dimensions", "specification": "98 x 78 x 53"},
        {"product_id": 29, "parameter_name": "VRM fan", "specification": "40mm PWM, 1000 - 3000 RPM"},
        {"product_id": 29, "parameter_name": "Manufacturer", "specification": "Arctic"},
        
        {"product_id": 30, "parameter_name": "Product Type", "specification": "CPU Liquid Cooling System"},
        {"product_id": 30, "parameter_name": "Radiator Dimensions", "specification": "140×310×28 mm"},
        {"product_id": 30, "parameter_name": "Radiator Dimensions with Fans", "specification": "140×310×54 mm"},
        {"product_id": 30, "parameter_name": "Material", "specification": "Aluminum"},
        {"product_id": 30, "parameter_name": "Number of Fans", "specification": "2"},
        {"product_id": 30, "parameter_name": "Fan Type", "specification": "Fluctus 140 PWM"},
        {"product_id": 30, "parameter_name": "Fan Dimensions", "specification": "140×140×25 mm"},
        {"product_id": 30, "parameter_name": "Fan Bearings", "specification": "FDB (Fluid Dynamic Bearing)"},
        {"product_id": 30, "parameter_name": "Fan Speed", "specification": "250 (±100) – 1800 (±10%) RPM"},
        {"product_id": 30, "parameter_name": "Fan Control (Speed)", "specification": "PWM (Pulse Width Modulation)"},
        {"product_id": 30, "parameter_name": "Fan Power Connector", "specification": "4-pin (male and female)"},
        {"product_id": 30, "parameter_name": "Fan Voltage", "specification": "12 V"},
        {"product_id": 30, "parameter_name": "Fan Current (Peak)", "specification": "0.30 A"},
        {"product_id": 30, "parameter_name": "Fan Lifespan", "specification": "100,000 hours"},
        {"product_id": 30, "parameter_name": "Cold Plate Base", "specification": "Copper"},
        {"product_id": 30, "parameter_name": "Bearing", "specification": "Ceramic"},
        {"product_id": 30, "parameter_name": "Pump Voltage", "specification": "12 V"},
        {"product_id": 30, "parameter_name": "Pump Current (Peak)", "specification": "0.33 A"},
        {"product_id": 30, "parameter_name": "Pump Control (Speed)", "specification": "PWM (Pulse Width Modulation)"},
        {"product_id": 30, "parameter_name": "Speed Connector (Pump)", "specification": "4-pin PWM (female)"},
        {"product_id": 30, "parameter_name": "Pump Speed", "specification": "1600 – 2600 (±10%) RPM"},
        {"product_id": 30, "parameter_name": "Power Connector (Pump)", "specification": "SATA"},
        {"product_id": 30, "parameter_name": "Compatibility with Processors", "specification": "AMD AM5, AM4Intel LGA1700, LGA1200, LGA1150, LGA1151,  LGA1155, LGA1156, LGA2066, LGA2011-3, LGA2011 (square ILM)"},

        {"product_id": 31, "parameter_name": "Number of Fans", "specification": "3 pcs"},
        {"product_id": 31, "parameter_name": "Fan Dimensions", "specification": "140mm"},
        {"product_id": 31, "parameter_name": "Speed Regulation", "specification": "PWM regulation"},
        {"product_id": 31, "parameter_name": "Minimum Fan Speed", "specification": "200 rpm"},
        {"product_id": 31, "parameter_name": "Maximum Fan Speed", "specification": "1700 rpm"},
        {"product_id": 31, "parameter_name": "Heat Sink Material", "specification": "Aluminum"},
        {"product_id": 31, "parameter_name": "Dimensions with Fans", "specification": "458 x 138 x 65.5 mm"},
        {"product_id": 31, "parameter_name": "Heat Sink Dimensions", "specification": "458 x 138 x 38 mm"},
        {"product_id": 31, "parameter_name": "Outer Diameter of Hoses", "specification": "12.4mm"},
        {"product_id": 31, "parameter_name": "Inner Diameter of Hoses", "specification": "6mm"},
        {"product_id": 31, "parameter_name": "Length of Hoses", "specification": "450mm"},
        {"product_id": 31, "parameter_name": "Pump Speed", "specification": "800 - 2800 rpm"},
        {"product_id": 31, "parameter_name": "Basis of Cooling", "specification": "Copper"},
        {"product_id": 31, "parameter_name": "Fans", "specification": "Arctic P14 PWM"},
        {"product_id": 31, "parameter_name": "Air Flow", "specification": "123.76 m3/h"},
        {"product_id": 31, "parameter_name": "Static Pressure", "specification": "2.40 mmH2O"},
        {"product_id": 31, "parameter_name": "Bearing", "specification": "Fluid Dynamic Bearing"},
        {"product_id": 31, "parameter_name": "Paste Included", "specification": "MX-6 8g"},
        {"product_id": 31, "parameter_name": "Intel Compatibility", "specification": "LGA1700"},
        {"product_id": 31, "parameter_name": "AMD Compatibility", "specification": "AM4, AM5"},
        {"product_id": 31, "parameter_name": "Weight", "specification": "2235 g"},

        {"product_id": 32, "parameter_name": "Number of Fans", "specification": "3 pcs"},
        {"product_id": 32, "parameter_name": "Fan Dimensions", "specification": "140mm"},
        {"product_id": 32, "parameter_name": "Speed Regulation", "specification": "PWM regulation"},
        {"product_id": 32, "parameter_name": "Minimum Fan Speed", "specification": "200 rpm"},
        {"product_id": 32, "parameter_name": "Maximum Fan Speed", "specification": "1900 rpm"},
        {"product_id": 32, "parameter_name": "Heat Sink Material", "specification": "Aluminum"},
        {"product_id": 32, "parameter_name": "Dimensions with Fans", "specification": "458 x 138 x 65.5 mm"},
        {"product_id": 32, "parameter_name": "Heat Sink Dimensions", "specification": "458 x 138 x 38 mm"},
        {"product_id": 32, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 32, "parameter_name": "Outer Diameter of Hoses", "specification": "12.4mm"},
        {"product_id": 32, "parameter_name": "Inner Diameter of Hoses", "specification": "6mm"},
        {"product_id": 32, "parameter_name": "Length of Hoses", "specification": "450mm"},
        {"product_id": 32, "parameter_name": "Pump Speed", "specification": "800 - 2800 rpm"},
        {"product_id": 32, "parameter_name": "Basis of Cooling", "specification": "Copper"},
        {"product_id": 32, "parameter_name": "Fans", "specification": "Arctic P14 PWM A-RGB"},
        {"product_id": 32, "parameter_name": "Air Flow", "specification": "117.06 m3/h"},
        {"product_id": 32, "parameter_name": "Static Pressure", "specification": "2.0mmH2O"},
        {"product_id": 32, "parameter_name": "Bearing", "specification": "Fluid Dynamic Bearing"},
        {"product_id": 32, "parameter_name": "Number of ARGB LEDs", "specification": "12x A-RGB"},
        {"product_id": 32, "parameter_name": "Paste Included", "specification": "MX-6 8g"},
        {"product_id": 32, "parameter_name": "Intel Compatibility", "specification": "LGA1700"},
        {"product_id": 32, "parameter_name": "AMD Compatibility", "specification": "AM4, AM5"},
        {"product_id": 32, "parameter_name": "Weight", "specification": "2325 g"},

        {"product_id": 33, "parameter_name": "Color", "specification": "White"},
        {"product_id": 33, "parameter_name": "Cooler Dimensions", "specification": "400 x 124 x 27 mm (L x W x H)"},
        {"product_id": 33, "parameter_name": "Material", "specification": "Aluminum, Plastic"},
        {"product_id": 33, "parameter_name": "Length of Hoses", "specification": "400 mm, Braided"},
        {"product_id": 33, "parameter_name": "Fan Type", "specification": "3x EK-Vardar 120 D-RGB (ARGB, 120 mm)"},
        {"product_id": 33, "parameter_name": "Fan Dimensions", "specification": "120 x 120 x 25 mm (L x W x H)"},
        {"product_id": 33, "parameter_name": "Plug Type", "specification": "4-pin PWM / 3-pin ARGB plug (5V)"},
        {"product_id": 33, "parameter_name": "Rotational Speed", "specification": "500 - 2,200 rpm"},
        {"product_id": 33, "parameter_name": "Air Flow", "specification": "131 m³/h"},
        {"product_id": 33, "parameter_name": "Static Pressure", "specification": "Max. 3.16 mmH2O"},
        {"product_id": 33, "parameter_name": "Volume", "specification": "33.5 dB(A)"},
        {"product_id": 33, "parameter_name": "Operating Voltage", "specification": "12V DC"},
        {"product_id": 33, "parameter_name": "Power Consumption", "specification": "2.16 W"},
        {"product_id": 33, "parameter_name": "MTTF (Fan)", "specification": "50,000 hours"},
        {"product_id": 33, "parameter_name": "Pump Dimensions", "specification": "61.6 x 69.2 x 82.3 mm (L x W x H)"},
        {"product_id": 33, "parameter_name": "Max Speed (Pump)", "specification": "3,100 rpm"},
        {"product_id": 33, "parameter_name": "Volume (Pump)", "specification": "18.5 dB(A)"},
        {"product_id": 33, "parameter_name": "Current Intensity (Pump)", "specification": "0.37 A"},
        {"product_id": 33, "parameter_name": "ARGB Backlight", "specification": "3-Pin RGB (5VDG, 5V)"},
        {"product_id": 33, "parameter_name": "Plug (Pump)", "specification": ">4-Pin PWM"},
        {"product_id": 33, "parameter_name": "MTTF (Pump)", "specification": "70,000 hours"},
        {"product_id": 33, "parameter_name": "Compatibility (Intel)", "specification": "LGA 1700, LGA 1200, LGA 115X, LGA 1366, LGA 775, LGA 2011,  LGA 2066"},
        {"product_id": 33, "parameter_name": "Compatibility (AMD)", "specification": "AM4, AM5"},

         {"product_id": 34, "parameter_name": "Color", "specification": "White"},
        {"product_id": 34, "parameter_name": "Cooler Dimensions", "specification": "400 x 124 x 27 mm (L x W x H)"},
        {"product_id": 34, "parameter_name": "Material", "specification": "Aluminum, Plastic"},
        {"product_id": 34, "parameter_name": "Length of Hoses", "specification": "400 mm, Braided"},
        {"product_id": 34, "parameter_name": "Fan Type", "specification": "3x EK-Vardar 120 D-RGB (ARGB, 120 mm)"},
        {"product_id": 34, "parameter_name": "Fan Dimensions", "specification": "120 x 120 x 25 mm (L x W x H)"},
        {"product_id": 34, "parameter_name": "Plug Type", "specification": "4-pin PWM / 3-pin ARGB plug (5V)"},
        {"product_id": 34, "parameter_name": "Rotational Speed", "specification": "500 - 2,200 rpm"},
        {"product_id": 34, "parameter_name": "Air Flow", "specification": "131 m³/h"},
        {"product_id": 34, "parameter_name": "Static Pressure", "specification": "Max. 3.16 mmH2O"},
        {"product_id": 34, "parameter_name": "Volume", "specification": "33.5 dB(A)"},
        {"product_id": 34, "parameter_name": "Operating Voltage", "specification": "12V DC"},
        {"product_id": 34, "parameter_name": "Power Consumption", "specification": "2.16 W"},
        {"product_id": 34, "parameter_name": "MTTF (Fan)", "specification": "50,000 hours"},
        {"product_id": 34, "parameter_name": "Pump Dimensions", "specification": "61.6 x 69.2 x 82.3 mm (L x W x H)"},
        {"product_id": 34, "parameter_name": "Max Speed (Pump)", "specification": "3,100 rpm"},
        {"product_id": 34, "parameter_name": "Volume (Pump)", "specification": "18.5 dB(A)"},
        {"product_id": 34, "parameter_name": "Current Intensity (Pump)", "specification": "0.37 A"},
        {"product_id": 34, "parameter_name": "ARGB Backlight", "specification": "3-Pin RGB (5VDG, 5V)"},
        {"product_id": 34, "parameter_name": "Plug (Pump)", "specification": ">4-Pin PWM"},
        {"product_id": 34, "parameter_name": "MTTF (Pump)", "specification": "70,000 hours"},
        {"product_id": 34, "parameter_name": "Compatibility (Intel)", "specification": "LGA 1700, LGA 1200, LGA 115X, LGA 1366, LGA 775, LGA 2011,  LGA 2066"},
        {"product_id": 34, "parameter_name": "Compatibility (AMD)", "specification": "AM4, AM5"},

        {"product_id": 35, "parameter_name": "Cooling Plate Material", "specification": "Copper"},
        {"product_id": 35, "parameter_name": "Heat Sink Material", "specification": "Aluminum"},
        {"product_id": 35, "parameter_name": "Tube Diameter", "specification": "6mm"},
        {"product_id": 35, "parameter_name": "Thickness of Heat Sink", "specification": "0.4mm"},
        {"product_id": 35, "parameter_name": "Radiator Fin Spacing", "specification": "2.15mm"},
        {"product_id": 35, "parameter_name": "Size", "specification": "125x109x1575mm"},
        {"product_id": 35, "parameter_name": "Tube Material", "specification": "Copper"},
        {"product_id": 35, "parameter_name": "Base Dimensions", "specification": "42x38mm"},
        {"product_id": 35, "parameter_name": "Fan Dimensions", "specification": "120x120x25mm"},
        {"product_id": 35, "parameter_name": "Fan Speed", "specification": "800-2150RPM± 10%"},
        {"product_id": 35, "parameter_name": "Number of Fans", "specification": "2"},
        {"product_id": 35, "parameter_name": "Operating Mode", "specification": "PWM"},
        {"product_id": 35, "parameter_name": "Manufacturing Process", "specification": "Reflow Soldering"},
        {"product_id": 35, "parameter_name": "RGB Lighting Type", "specification": "ARGB"},
        {"product_id": 35, "parameter_name": "Fan Model", "specification": "Valkyrie X12"},
        {"product_id": 35, "parameter_name": "Fan Airflow", "specification": "80CFM (Max)"},
        {"product_id": 35, "parameter_name": "Fan Static Pressure", "specification": "2.23mmH2O (Max)"},
        {"product_id": 35, "parameter_name": "Noise Level", "specification": "≤29dBA (Max)"},
        {"product_id": 35, "parameter_name": "Compatibility with Intel", "specification": "1150, 1151, 1155, 1156, 1200, 1700, 2011, 2011-3, 2066, 1700"},
        {"product_id": 35, "parameter_name": "Compatibility with AMD Sockets", "specification": "AM4, AM5"},

        {"product_id": 36, "parameter_name": "Dimensions", "specification": "93 x 126 x 78 mm (W x H x D)"},
        {"product_id": 36, "parameter_name": "Weight", "specification": "Approximately 450g"},
        {"product_id": 36, "parameter_name": "Material", "specification": "Copper, Aluminum, Plastic"},
        {"product_id": 36, "parameter_name": "TDP", "specification": "130W"},
        {"product_id": 36, "parameter_name": "Fan", "specification": "Number: 1x 92 mm  Speed: 900 - 2300 rpm  Max Airflow: 61.1 m³/h  Noise Level: 20 - 30.5 dB(A)  Plug: 4-pin PWM  Voltage: 12V  Number of Heat Pipes: 4x 6 mm"},
        {"product_id": 36, "parameter_name": "Compatibility", "specification": "Intel: 775, 1150, 1151, 1155, 1156  AMD: AM2, AM2+, AM3, AM3+, AM4, AM5, FM1, FM2, FM2+"},

        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "165 mm"},
        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "150 mm"},
        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "52 mm"},
        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "165 mm"},
        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "150 mm"},
        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "78 mm"},
        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "935 g"},
        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "Copper (base and heat pipes), Aluminum (radiator)"},
        {"product_id": 37, "parameter_name": "Rozmiar", "specification": "140x150x25 (120mm mounting holes), 140x140x25 (120mm mounting holes), 120x120x25mm"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "1x Noctua NF-A15 PWM"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "SSO2"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "(+/- 10%) 1500 RPM"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "(+/- 10%) 1200 RPM"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "(+/-20%) 300 RPM"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "140.2 m³/h"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "115.5 m³/h"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "24.6 dB(A)"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "19.2 dB(A)"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "Black NH-U14S heatsink, 1x NF-A15 PWM, 1x Low-Noise Adaptor  (L.N.A), NT-H1 high-grade thermal compound, Black SecuFirm2™  mounting kit, Noctua Metal Case-Badge"},
        {"product_id": 37, "parameter_name": "chipset", "specification": "Intel: LGA1700, LGA1200, LGA1156, LGA1155, LGA1151, LGA1150, LGA2066, LGA2011-0, LGA2011-3 (Square ILM)  AMD: AM4, AM5"},

        {"product_id": 38, "parameter_name": "Product Type", "specification": "PC Case"},
        {"product_id": 38, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 38, "parameter_name": "Dimensions (H x W x D)", "specification": "486 x 228 x 429 mm"},
        {"product_id": 38, "parameter_name": "Motherboard Standard", "specification": "ATX, microATX, ITX"},
        {"product_id": 38, "parameter_name": "Maximum GPU Length", "specification": "350 mm"},
        {"product_id": 38, "parameter_name": "Maximum CPU Cooler Height", "specification": "179 mm"},
        {"product_id": 38, "parameter_name": "Maximum PSU Length", "specification": "300 mm"},
        {"product_id": 38, "parameter_name": "Expansion Card Slots", "specification": "7"},
        {"product_id": 38, "parameter_name": "Number of Drive Bays", "specification": "1 x 2.5”/3.5”, 6 x 2.5”"},
        {"product_id": 38, "parameter_name": "Maximum Number of Fans", "specification": "4"},
        {"product_id": 38, "parameter_name": "Maximum Number of Fans", "specification": "7"},
        {"product_id": 38, "parameter_name": "Fans Included", "specification": "Front: 3 x Stratus 140 PWM fan (200–1200 rpm)  Back: 1 x Stratus 140 PWM fan (200–1200 rpm)"},
        {"product_id": 38, "parameter_name": "Liquid Cooling Radiator", "specification": "Front: 1 x 120, 240, 280, 360 mm  Top: 1 x 120, 240, 280 mm  Rear: 1 x 120, 140 mm"},
        {"product_id": 38, "parameter_name": "Dust Filters", "specification": "Front, Top, Bottom"},
        {"product_id": 38, "parameter_name": "I/O Panel", "specification": "1 x USB-C  2 x USB-A  1 x Headphones (3.5 mm minijack)  1 x Microphone (3.5 mm minijack)  1 x POWER button  1 x RESET/LED button"},

        {"product_id": 39, "parameter_name": "Product Designation", "specification": "P.C Gaming"},
        {"product_id": 39, "parameter_name": "Capacity", "specification": "1000 GB"},
        {"product_id": 39, "parameter_name": "Format", "specification": "M.2"},
        {"product_id": 39, "parameter_name": "Interface", "specification": "PCIe NVMe 4.0 x4"},
        {"product_id": 39, "parameter_name": "Maximum Reading Speed", "specification": "7500 MB/s"},
        {"product_id": 39, "parameter_name": "Maximum Write Speed", "specification": "6300 MB/s"},
        {"product_id": 39, "parameter_name": "Random Reading", "specification": "1,000,000 IOPS"},
        {"product_id": 39, "parameter_name": "Random Recording", "specification": "1,100,000 IOPS"},
        {"product_id": 39, "parameter_name": "MTBF Reliability", "specification": "1,500,000 hours"},
        {"product_id": 39, "parameter_name": "Radiator", "specification": "NO"},
        {"product_id": 39, "parameter_name": "Additional Information", "specification": "Increased vibration resistance"},
        {"product_id": 39, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 39, "parameter_name": "Height", "specification": "2.45 mm"},
        {"product_id": 39, "parameter_name": "Width", "specification": "22 mm"},
        {"product_id": 39, "parameter_name": "Depth", "specification": "80 mm"},
        {"product_id": 39, "parameter_name": "Weight", "specification": "9 g"},
        {"product_id": 39, "parameter_name": "Guarantee", "specification": "60 months (manufacturers warranty)"},

        {"product_id": 40, "parameter_name": "Product Designation", "specification": "P.C Gaming PlayStation 5"},
        {"product_id": 40, "parameter_name": "Capacity", "specification": "1000 GB"},
        {"product_id": 40, "parameter_name": "Format", "specification": "M.2"},
        {"product_id": 40, "parameter_name": "Interface", "specification": "PCIe NVMe 4.0 x4"},
        {"product_id": 40, "parameter_name": "Maximum Reading Speed", "specification": "7400 MB/s"},
        {"product_id": 40, "parameter_name": "Maximum Write Speed", "specification": "6500 MB/s"},
        {"product_id": 40, "parameter_name": "Random Reading", "specification": "1,000,000 IOPS"},
        {"product_id": 40, "parameter_name": "Random Recording", "specification": "900,000 IOPS"},
        {"product_id": 40, "parameter_name": "MTBF Reliability", "specification": "1,500,000 hours"},
        {"product_id": 40, "parameter_name": "Additional Information", "specification": "Increased vibration resistance, Compatible with PlayStation  5"},
        {"product_id": 40, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 40, "parameter_name": "Height", "specification": "2.45 mm"},
        {"product_id": 40, "parameter_name": "Width", "specification": "22 mm"},
        {"product_id": 40, "parameter_name": "Depth", "specification": "80 mm"},
        {"product_id": 40, "parameter_name": "Weight", "specification": "6 g"},
        {"product_id": 40, "parameter_name": "Guarantee", "specification": "60 months (manufacturers warranty)"},
        {"product_id": 40, "parameter_name": "Manufacturer Code", "specification": "LNM790X001T-RNNNG"},

        {"product_id": 41, "parameter_name": "Product Designation", "specification": "P.C Gaming"},
        {"product_id": 41, "parameter_name": "Capacity", "specification": "1000 GB"},
        {"product_id": 41, "parameter_name": "Format", "specification": "M.2"},
        {"product_id": 41, "parameter_name": "Interface", "specification": "PCIe NVMe 4.0 x4"},
        {"product_id": 41, "parameter_name": "Maximum Reading Speed", "specification": "5000 MB/s"},
        {"product_id": 41, "parameter_name": "Maximum Write Speed", "specification": "4500 MB/s"},
        {"product_id": 41, "parameter_name": "MTBF Reliability", "specification": "1,500,000 hours"},
        {"product_id": 41, "parameter_name": "TBW Factor", "specification": "600 TB"},
        {"product_id": 41, "parameter_name": "Radiator", "specification": "NO"},
        {"product_id": 41, "parameter_name": "Additional Information", "specification": "SLC technology, Vibration and drop resistant"},
        {"product_id": 41, "parameter_name": "Color", "specification": "Black and blue"},
        {"product_id": 41, "parameter_name": "Height", "specification": "2.45 mm"},
        {"product_id": 41, "parameter_name": "Width", "specification": "22 mm"},
        {"product_id": 41, "parameter_name": "Depth", "specification": "80 mm"},
        {"product_id": 41, "parameter_name": "Weight", "specification": "7 g"},
        {"product_id": 41, "parameter_name": "Guarantee", "specification": "60 months (manufacturers warranty)"},
        {"product_id": 41, "parameter_name": "Manufacturer Code", "specification": "LNM710X001T-RNNNG"},

        {"product_id": 42, "parameter_name": "Product Designation", "specification": "P.C Gaming"},
        {"product_id": 42, "parameter_name": "Capacity", "specification": "1000 GB"},
        {"product_id": 42, "parameter_name": "Format", "specification": "M.2"},
        {"product_id": 42, "parameter_name": "Interface", "specification": "PCIe NVMe 3.0 x4"},
        {"product_id": 42, "parameter_name": "Maximum Reading Speed", "specification": "3300 MB/s"},
        {"product_id": 42, "parameter_name": "Maximum Write Speed", "specification": "3000 MB/s"},
        {"product_id": 42, "parameter_name": "Random Reading", "specification": "300,000 IOPS"},
        {"product_id": 42, "parameter_name": "Random Recording", "specification": "256,000 IOPS"},
        {"product_id": 42, "parameter_name": "Type of Memory", "specification": "TLC"},
        {"product_id": 42, "parameter_name": "MTBF Reliability", "specification": "1,500,000 hours"},
        {"product_id": 42, "parameter_name": "TBW Factor", "specification": "500 TB"},
        {"product_id": 42, "parameter_name": "Radiator", "specification": "NO"},
        {"product_id": 42, "parameter_name": "Additional Information", "specification": "LDPC technology"},
        {"product_id": 42, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 42, "parameter_name": "Height", "specification": "2.25 mm"},
        {"product_id": 42, "parameter_name": "Width", "specification": "22 mm"},
        {"product_id": 42, "parameter_name": "Depth", "specification": "80 mm"},
        {"product_id": 42, "parameter_name": "Weight", "specification": "9 g"},
        {"product_id": 42, "parameter_name": "Guarantee", "specification": "60 months (manufacturers warranty)"},
        {"product_id": 42, "parameter_name": "Manufacturer Code", "specification": "LNM620X001T-RNNNG"},

        {"product_id": 43, "parameter_name": "Capacity", "specification": "2000 GB"},
        {"product_id": 43, "parameter_name": "Format", "specification": "M.2"},
        {"product_id": 43, "parameter_name": "Interface", "specification": "PCIe NVMe 4.0 x4"},
        {"product_id": 43, "parameter_name": "Maximum Reading Speed", "specification": "7300 MB/s"},
        {"product_id": 43, "parameter_name": "Maximum Write Speed", "specification": "6400 MB/s"},
        {"product_id": 43, "parameter_name": "Random Reading", "specification": "1,000,000 IOPS"},
        {"product_id": 43, "parameter_name": "Random Recording", "specification": "950,000 IOPS"},
        {"product_id": 43, "parameter_name": "MTBF Reliability", "specification": "1,500,000 hours"},
        {"product_id": 43, "parameter_name": "TBW Factor", "specification": "1200 TB"},
        {"product_id": 43, "parameter_name": "Radiator", "specification": "NO"},
        {"product_id": 43, "parameter_name": "Additional Information", "specification": "LDPC technology, TRIM technology, APST technology, SMART  technology"},
        {"product_id": 43, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 43, "parameter_name": "Height", "specification": "2 mm"},
        {"product_id": 43, "parameter_name": "Width", "specification": "22 mm"},
        {"product_id": 43, "parameter_name": "Depth", "specification": "80 mm"},
        {"product_id": 43, "parameter_name": "Guarantee", "specification": "60 months (manufacturers warranty)"},
        {"product_id": 43, "parameter_name": "Manufacturer Code", "specification": "S78-440Q730-P83"},

        {"product_id": 44, "parameter_name": "Disk Type", "specification": "SSD"},
        {"product_id": 44, "parameter_name": "Disk Format", "specification": "M.2 2280"},
        {"product_id": 44, "parameter_name": "Capacity", "specification": "1TB"},
        {"product_id": 44, "parameter_name": "Interface", "specification": "PCIe Gen 4.0 x4"},
        {"product_id": 44, "parameter_name": "Maximum Read Speed", "specification": "7450 MB/s"},
        {"product_id": 44, "parameter_name": "Maximum Write Speed", "specification": "6600 MB/s"},
        {"product_id": 44, "parameter_name": "Random Read", "specification": "860,000 IOPS"},
        {"product_id": 44, "parameter_name": "Random Write", "specification": "690,000 IOPS"},
        {"product_id": 44, "parameter_name": "MTBF Reliability", "specification": "2,000,000 hours"},
        {"product_id": 44, "parameter_name": "Operating Temperature", "specification": "0°C to 70°C"},
        {"product_id": 44, "parameter_name": "Storage Temperature", "specification": "-40°C to 85°C"},
        {"product_id": 44, "parameter_name": "Weight", "specification": "7 g"},
        {"product_id": 44, "parameter_name": "Manufacturers Warranty", "specification": "60 months"},

        {"product_id": 45, "parameter_name": "Product Designation", "specification": "P.C"},
        {"product_id": 45, "parameter_name": "Capacity", "specification": "2048GB"},
        {"product_id": 45, "parameter_name": "Format", "specification": "2.5\""},
        {"product_id": 45, "parameter_name": "Interface", "specification": "2.5\" SATA"},
        {"product_id": 45, "parameter_name": "Maximum Reading Speed", "specification": "550MB/s"},
        {"product_id": 45, "parameter_name": "Maximum Writing Speed", "specification": "500MB/s"},
        {"product_id": 45, "parameter_name": "MTBF Reliability", "specification": "2,000,000 hours"},
        {"product_id": 45, "parameter_name": "TBW Factor", "specification": "720TB"},
        {"product_id": 45, "parameter_name": "Radiator", "specification": "NO"},
        {"product_id": 45, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 45, "parameter_name": "Height", "specification": "7mm"},
        {"product_id": 45, "parameter_name": "Width", "specification": "69.85mm"},
        {"product_id": 45, "parameter_name": "Depth", "specification": "100mm"},
        {"product_id": 45, "parameter_name": "Weight", "specification": "9 g"},
        {"product_id": 45, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 45, "parameter_name": "Manufacturer Code", "specification": "SSDPR-CX400-02T-G2"},

        {"product_id": 46, "parameter_name": "Product Designation", "specification": "P.C"},
        {"product_id": 46, "parameter_name": "Capacity", "specification": "2048GB"},
        {"product_id": 46, "parameter_name": "Format", "specification": '2.5"'},
        {"product_id": 46, "parameter_name": 'Interface', "specification": '2.5" SATA'},
        {"product_id": 46, "parameter_name": "Maximum Reading Speed", "specification": "550MB/s"},
        {"product_id": 46, "parameter_name": "Maximum Writing Speed", "specification": "500MB/s"},
        {"product_id": 46, "parameter_name": "MTBF Reliability", "specification": "2,000,000 hours"},
        {"product_id": 46, "parameter_name": "TBW Factor", "specification": "720TB"},
        {"product_id": 46, "parameter_name": "Radiator", "specification": "NO"},
        {"product_id": 46, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 46, "parameter_name": "Height", "specification": "7mm"},
        {"product_id": 46, "parameter_name": "Width", "specification": "69.85mm"},
        {"product_id": 46, "parameter_name": "Depth", "specification": "100mm"},
        {"product_id": 46, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 46, "parameter_name": "Manufacturer Code", "specification": "SSDPR-CX400-02T-G2"},

        {"product_id": 47, "parameter_name": "Capacity", "specification": "1000 GB"},
        {"product_id": 47, "parameter_name": "Format", "specification": '3.5"'},
        {"product_id": 47, "parameter_name": "Interface", "specification": "SATA III (6.0 Gb/s) - 1 pc."},
        {"product_id": 47, "parameter_name": "Cache memory", "specification": "64 MB"},
        {"product_id": 47, "parameter_name": "Rotation speed", "specification": "7200 rpm"},
        {"product_id": 47, "parameter_name": "Height", "specification": "26.1 mm"},
        {"product_id": 47, "parameter_name": "Width", "specification": "101.6 mm"},
        {"product_id": 47, "parameter_name": "Depth", "specification": "147 mm"},
        {"product_id": 47, "parameter_name": "Weight", "specification": "450 g"},
        {"product_id": 47, "parameter_name": "Warranty", "specification": "24 months (manufacturer's warranty)"},
        {"product_id": 47, "parameter_name": "Manufacturer's code", "specification": "HDWD110EZSTA"},

        {"product_id": 48, "parameter_name": "Size", "specification": "120 x 120 mm"},
        {"product_id": 48, "parameter_name": "Rotation speed", "specification": "1800 rpm"},
        {"product_id": 48, "parameter_name": "Maximum air flow", "specification": "61.7 CFM"},
        {"product_id": 48, "parameter_name": "Backlight", "specification": "Lack"},
        {"product_id": 48, "parameter_name": "Quantity", "specification": "3"},
        {"product_id": 48, "parameter_name": "Bearing type", "specification": "Hydraulic Bearing System"},
        {"product_id": 48, "parameter_name": "Supply voltage", "specification": "12 V"},
        {"product_id": 48, "parameter_name": "Current", "specification": "0.15 A"},
        {"product_id": 48, "parameter_name": "Connector", "specification": "4 pin plug"},
        {"product_id": 48, "parameter_name": "Service life", "specification": "50000 hours"},
        {"product_id": 48, "parameter_name": "Dimensions", "specification": "120 x 120 x 25 mm"},
        {"product_id": 48, "parameter_name": "Housing color", "specification": "Black"},
        {"product_id": 48, "parameter_name": "Additional information", "specification": "Anti-vibration rubber bands"},
        {"product_id": 48, "parameter_name": "Additional accessories", "specification": "Screws4-pin PWM splitter"},
        {"product_id": 48, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 48, "parameter_name": "Manufacturer code", "specification": "SMXC004"},

        {"product_id": 49, "parameter_name": "Size", "specification": "120 x 120 mm"},
        {"product_id": 49, "parameter_name": "Rotation speed", "specification": "1500 rpm"},
        {"product_id": 49, "parameter_name": "Maximum air flow", "specification": "68.2 CFM"},
        {"product_id": 49, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 49, "parameter_name": "Quantity", "specification": "1"},
        {"product_id": 49, "parameter_name": "Bearing type", "specification": "Hydraulic Bearing System"},
        {"product_id": 49, "parameter_name": "Supply voltage", "specification": "5V - 12V"},
        {"product_id": 49, "parameter_name": "Current", "specification": "0.25A (normal) 0.5A (ARGB)"},
        {"product_id": 49, "parameter_name": "Connector", "specification": "4 pin plug + 3 pin ARGB"},
        {"product_id": 49, "parameter_name": "Service life", "specification": "50000 hours"},
        {"product_id": 49, "parameter_name": "Dimensions", "specification": "120 x 120 x 25 mm"},
        {"product_id": 49, "parameter_name": "Housing color", "specification": "White"},
        {"product_id": 49, "parameter_name": "Additional information", "specification": "Anti-vibration rubber bands"},
        {"product_id": 49, "parameter_name": "Additional accessories", "specification": "Screws ARGB 3-pin male connector bridge"},
        {"product_id": 49, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 49, "parameter_name": "Manufacturer Code", "specification": "SMXC007"},
        
        {"product_id": 50, "parameter_name": "Size", "specification": "120 x 120 mm"},
        {"product_id": 50, "parameter_name": "Rotation speed", "specification": "1600 rpm"},
        {"product_id": 50, "parameter_name": "Maximum noise level", "specification": "18.9 dB"},
        {"product_id": 50, "parameter_name": "Maximum air flow", "specification": "48.7 CFM"},
        {"product_id": 50, "parameter_name": "Backlight", "specification": "Lack"},
        {"product_id": 50, "parameter_name": "Quantity", "specification": "1"},
        {"product_id": 50, "parameter_name": "Bearing type", "specification": "Fluid Dynamic Bearing"},
        {"product_id": 50, "parameter_name": "Supply voltage", "specification": "5V - 13.2V"},
        {"product_id": 50, "parameter_name": "Current", "specification": "0.12A"},
        {"product_id": 50, "parameter_name": "Connector", "specification": "4 pin plug"},
        {"product_id": 50, "parameter_name": "Service life", "specification": "300000 hours"},
        {"product_id": 50, "parameter_name": "Dimensions", "specification": "120 x 120 x 25 mm"},
        {"product_id": 50, "parameter_name": "Housing color", "specification": "Black"},
        {"product_id": 50, "parameter_name": "Additional information", "specification": "Anti-vibration rubber bands Blades with optimized shape"},
        {"product_id": 50, "parameter_name": "Additional accessories", "specification": "Screws Silicone pads Anti-vibration pins"},
        {"product_id": 50, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 50, "parameter_name": "Manufacturer Code", "specification": "BL093"},
        

        {"product_id": 51, "parameter_name": "Size", "specification": "120 x 120 mm"},
        {"product_id": 51, "parameter_name": "Rotation speed", "specification": "2000 rpm"},
        {"product_id": 51, "parameter_name": "Maximum noise level", "specification": "32.7 dB"},
        {"product_id": 51, "parameter_name": "Maximum air flow", "specification": "85.71 CFM"},
        {"product_id": 51, "parameter_name": "Backlight", "specification": "RGB"},
        {"product_id": 51, "parameter_name": "Bearing type", "specification": "Long Life Sleeve (LLS)"},
        {"product_id": 51, "parameter_name": "Supply voltage", "specification": "7V - 12V"},
        {"product_id": 51, "parameter_name": "Current", "specification": "0.18A"},
        {"product_id": 51, "parameter_name": "Connector", "specification": "4 pin plug"},
        {"product_id": 51, "parameter_name": "Service life", "specification": "100000 hours"},
        {"product_id": 51, "parameter_name": "Dimensions", "specification": "120 x 120 x 25 mm"},
        {"product_id": 51, "parameter_name": "Housing color", "specification": "Black"},
        {"product_id": 51, "parameter_name": "Additional information", "specification": "RGB backlight Anti-vibration rubber bands Blades with optimized shape Braided cable"},
        {"product_id": 51, "parameter_name": "Additional accessories", "specification": "Screws"},
        {"product_id": 51, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 51, "parameter_name": "Manufacturer Code", "specification": "FD-FAN-PRI-AL12-PWM"},

        {"product_id": 52, "parameter_name": "Size", "specification": "140 x 140 mm"},
        {"product_id": 52, "parameter_name": "Rotation speed", "specification": "1700 rpm"},
        {"product_id": 52, "parameter_name": "Maximum noise level", "specification": "35.5 dB"},
        {"product_id": 52, "parameter_name": "Maximum air flow", "specification": "78 CFM"},
        {"product_id": 52, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 52, "parameter_name": "Bearing type", "specification": "Rifle"},
        {"product_id": 52, "parameter_name": "Supply voltage", "specification": "12V"},
        {"product_id": 52, "parameter_name": "Current", "specification": "0.24A"},
        {"product_id": 52, "parameter_name": "Connector", "specification": "4 pin plug + 3 pin ARGB"},
        {"product_id": 52, "parameter_name": "Service life", "specification": "90000 hours"},
        {"product_id": 52, "parameter_name": "Dimensions", "specification": "140 x 140 x 25 mm"},
        {"product_id": 52, "parameter_name": "Housing color", "specification": "Black"},
        {"product_id": 52, "parameter_name": "Additional information", "specification": "Ribbon cable"},
        {"product_id": 52, "parameter_name": "Additional accessories", "specification": "Screws"},
        {"product_id": 52, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 52, "parameter_name": "Manufacturer Code", "specification": "FD-F-AS1-1405"},  

        {"product_id": 53, "parameter_name": "Size", "specification": "140 x 140 mm"},
        {"product_id": 53, "parameter_name": "Rotation speed", "specification": "1700 rpm"},
        {"product_id": 53, "parameter_name": "Maximum noise level", "specification": "35.5 dB"},
        {"product_id": 53, "parameter_name": "Maximum air flow", "specification": "78 CFM"},
        {"product_id": 53, "parameter_name": "Backlight", "specification": "ARGB"},
        {"product_id": 53, "parameter_name": "Bearing type", "specification": "Rifle"},
        {"product_id": 53, "parameter_name": "Supply voltage", "specification": "12V"},
        {"product_id": 53, "parameter_name": "Current", "specification": "0.24A"},
        {"product_id": 53, "parameter_name": "Connector", "specification": "4 pin plug + 3 pin ARGB"},
        {"product_id": 53, "parameter_name": "Service life", "specification": "90000 hours"},
        {"product_id": 53, "parameter_name": "Dimensions", "specification": "140 x 140 x 25 mm"},
        {"product_id": 53, "parameter_name": "Housing color", "specification": "Black"},
        {"product_id": 53, "parameter_name": "Additional information", "specification": "Ribbon cable"},
        {"product_id": 53, "parameter_name": "Additional accessories", "specification": "Screws"},
        {"product_id": 53, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 53, "parameter_name": "Manufacturer Code", "specification": "FD-F-AS1-1405"}, 

        {"product_id": 54, "parameter_name": "Size", "specification": "120 x 120 mm"},
        {"product_id": 54, "parameter_name": "Rotation speed", "specification": "1500 rpm"},
        {"product_id": 54, "parameter_name": "Maximum noise level", "specification": "24.8 dB"},
        {"product_id": 54, "parameter_name": "Maximum air flow", "specification": "43.25 CFM"},
        {"product_id": 54, "parameter_name": "Backlight", "specification": "RGB"},
        {"product_id": 54, "parameter_name": "Quantity", "specification": "3"},
        {"product_id": 54, "parameter_name": "Bearing type", "specification": "Hydraulic Bearing System"},
        {"product_id": 54, "parameter_name": "Supply voltage", "specification": "7V - 13.2V"},
        {"product_id": 54, "parameter_name": "Current", "specification": "0.3 A"},
        {"product_id": 54, "parameter_name": "Connector", "specification": "4 pin plug"},
        {"product_id": 54, "parameter_name": "Dimensions", "specification": "120 x 120 x 25 mm"},
        {"product_id": 54, "parameter_name": "Housing color", "specification": "Black"},
        {"product_id": 54, "parameter_name": "Additional information", "specification": "RGB backlight"},
        {"product_id": 54, "parameter_name": "Additional accessories", "specification": "Controller"},
        {"product_id": 54, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 54, "parameter_name": "Manufacturer Code", "specification": "CO-9050072-WW"},

        {"product_id": 55, "parameter_name": "Size", "specification": "120 x 120 mm"},
        {"product_id": 55, "parameter_name": "Rotation speed", "specification": "1500 rpm"},
        {"product_id": 55, "parameter_name": "Maximum noise level", "specification": "26 dB"},
        {"product_id": 55, "parameter_name": "Maximum air flow", "specification": "41.8 CFM"},
        {"product_id": 55, "parameter_name": "Backlight", "specification": "RGB"},
        {"product_id": 55, "parameter_name": "Quantity", "specification": "3"},
        {"product_id": 55, "parameter_name": "Bearing type", "specification": "Hydraulic Bearing System"},
        {"product_id": 55, "parameter_name": "Supply voltage", "specification": "6V - 13.2V"},
        {"product_id": 55, "parameter_name": "Current", "specification": "0.3 A"},
        {"product_id": 55, "parameter_name": "Connector", "specification": "4 pin plug + 4 pin RGB"},
        {"product_id": 55, "parameter_name": "Dimensions", "specification": "120 x 120 x 25 mm"},
        {"product_id": 55, "parameter_name": "Housing color", "specification": "Black"},
        {"product_id": 55, "parameter_name": "Additional accessories", "specification": "Screws, Controller"},
        {"product_id": 55, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 55, "parameter_name": "Manufacturer Code", "specification": "CO-9050098-WW"}, 

        {"product_id": 56, "parameter_name": "Size", "specification": "120 x 120 mm"},
        {"product_id": 56, "parameter_name": "Rotation speed", "specification": "2200 rpm"},
        {"product_id": 56, "parameter_name": "Maximum noise level", "specification": "36 dB"},
        {"product_id": 56, "parameter_name": "Maximum air flow", "specification": "63 CFM"},
        {"product_id": 56, "parameter_name": "Backlight", "specification": "RGB"},
        {"product_id": 56, "parameter_name": "Quantity", "specification": "3"},
        {"product_id": 56, "parameter_name": "Bearing type", "specification": "Hydraulic Bearing System"},
        {"product_id": 56, "parameter_name": "Supply voltage", "specification": "7V - 13.2V"},
        {"product_id": 56, "parameter_name": "Current", "specification": "0.3A"},
        {"product_id": 56, "parameter_name": "Connector", "specification": "4 pin plug + 4 pin RGB"},
        {"product_id": 56, "parameter_name": "Dimensions", "specification": "120 x 120 x 25 mm"},
        {"product_id": 56, "parameter_name": "Housing color", "specification": "White"},
        {"product_id": 56, "parameter_name": "Additional information", "specification": "RGB backlight"},
        {"product_id": 56, "parameter_name": "Additional accessories", "specification": "Screws, Controller"},
        {"product_id": 56, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 56, "parameter_name": "Manufacturer Code", "specification": "CO-9050092-WW"}, 

        {"product_id": 57, "parameter_name": "Graphics card series", "specification": "GeForce RTX 40 series"},
        {"product_id": 57, "parameter_name": "Ray tracing support", "specification": "Yes"},
        {"product_id": 57, "parameter_name": "Upscaling technique", "specification": "Nvidia DLSS 3.5"},
        {"product_id": 57, "parameter_name": "Graphic layout", "specification": "GeForce RTX 4060"},
        {"product_id": 57, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16 (x8 mode)"},
        {"product_id": 57, "parameter_name": "Memory", "specification": "8GB"},
        {"product_id": 57, "parameter_name": "A type of memory", "specification": "GDDR6"}, 
        {"product_id": 57, "parameter_name": "Memory bus", "specification": "128 bit"},
        {"product_id": 57, "parameter_name": "Core clock", "specification": "2505MHz"},
        {"product_id": 57, "parameter_name": "CUDA cores", "specification": "3072"},
        {"product_id": 57, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 57, "parameter_name": "Number of fans", "specification": "3"},
        {"product_id": 57, "parameter_name": "Types of outputs", "specification": "HDMI 2.1 - 2 pcs.DisplayPort 1.4 - 2 pcs."},
        {"product_id": 57, "parameter_name": "Number of monitors supported", "specification": "4"},
        {"product_id": 57, "parameter_name": "Supported libraries", "specification": "DirectX 12 UltimateOpenGL 4.6"},
        {"product_id": 57, "parameter_name": "Power connector", "specification": "8 pin - 1 pc."},
        {"product_id": 57, "parameter_name": "Recommended power supply power", "specification": "450 W"},
        {"product_id": 57, "parameter_name": "Length", "specification": "272 mm"},
        {"product_id": 57, "parameter_name": "Width", "specification": "115mm"},
        {"product_id": 57, "parameter_name": "Height", "specification": "40mm"},
        {"product_id": 57, "parameter_name": "PCB format", "specification": "ATX"},
        {"product_id": 57, "parameter_name": "Number of occupied slots", "specification": "Dual slot"},
        {"product_id": 57, "parameter_name": "Accessories included", "specification": "User manual"},
        {"product_id": 57, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 57, "parameter_name": "Manufacturer Code", "specification": "GV-N4060EAGLE OC-8GD"},

        {"product_id": 58, "parameter_name": "Graphics card series", "specification": "GeForce RTX 40 series"},
        {"product_id": 58, "parameter_name": "Ray tracing support", "specification": "Yes"},
        {"product_id": 58, "parameter_name": "Upscaling technique", "specification": "Nvidia DLSS 3.5"},
        {"product_id": 58, "parameter_name": "Graphic layout", "specification": "GeForce RTX 4060 Ti"},
        {"product_id": 58, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16 (x8 mode)"},
        {"product_id": 58, "parameter_name": "Memory", "specification": "16GB"},
        {"product_id": 58, "parameter_name": "A type of memory", "specification": "GDDR6"},
        {"product_id": 58, "parameter_name": "Memory bus", "specification": "128 bit"},
        {"product_id": 58, "parameter_name": "Core clock in boost mode", "specification": "2670MHz"},
        {"product_id": 58, "parameter_name": "Core clock in Gaming Mode", "specification": "2685 MHz"},
        {"product_id": 58, "parameter_name": "CUDA cores", "specification": "4352"},
        {"product_id": 58, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 58, "parameter_name": "Number of fans", "specification": "3"},
        {"product_id": 58, "parameter_name": "Backlight", "specification": "Yes"},
        {"product_id": 58, "parameter_name": "Types of outputs", "specification": "HDMI 2.1a - 1 pc.DisplayPort 1.4a - 3 pcs."},
        {"product_id": 58, "parameter_name": "Number of monitors supported", "specification": "4"},
        {"product_id": 58, "parameter_name": "Supported libraries", "specification": "DirectX 12 UltimateOpenGL 4.6"},
        {"product_id": 58, "parameter_name": "Power connector", "specification": "8 pin - 1 pc."},
        {"product_id": 58, "parameter_name": "Recommended power supply power", "specification": "550 W"},
        {"product_id": 58, "parameter_name": "Power consumption", "specification": "165 W"},
        {"product_id": 58, "parameter_name": "Length", "specification": "307mm"},
        {"product_id": 58, "parameter_name": "Width", "specification": "125 mm"},
        {"product_id": 58, "parameter_name": "Height", "specification": "46mm"},
        {"product_id": 58, "parameter_name": "Number of occupied slots", "specification": "Dual slot"},
        {"product_id": 58, "parameter_name": "Accessories included", "specification": "User manual"},
        {"product_id": 58, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 58, "parameter_name": "Manufacturer code", "specification": "RTX 4060 Ti GAMING X SLIM 16G"},
        {"product_id": 59, "parameter_name": "Ray tracing support", "specification": "Yes"},
        
        {"product_id": 59, "parameter_name": "Upscaling technique", "specification": "Nvidia DLSS 3.5"},
        {"product_id": 59, "parameter_name": "Graphic layout", "specification": "GeForce RTX 3060"},
        {"product_id": 59, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16"},
        {"product_id": 59, "parameter_name": "Memory", "specification": "12GB"},
        {"product_id": 59, "parameter_name": "A type of memory", "specification": "GDDR6"},
        {"product_id": 59, "parameter_name": "Memory bus", "specification": "192 bit"},
        {"product_id": 59, "parameter_name": "Efficient memory clocking", "specification": "15000MHz"},
        {"product_id": 59, "parameter_name": "Core clock", "specification": "1837MHz"},
        {"product_id": 59, "parameter_name": "CUDA cores", "specification": "3584"},
        {"product_id": 59, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 59, "parameter_name": "Types of outputs", "specification": "HDMI - 2 pcs.DisplayPort - 2 pcs."},
        {"product_id": 59, "parameter_name": "Supported libraries", "specification": "DirectX 12OpenGL 4.6"},
        {"product_id": 59, "parameter_name": "Power connector", "specification": "8 pin - 1 pc."},
        {"product_id": 59, "parameter_name": "Recommended power supply power", "specification": "550 W"},
        {"product_id": 59, "parameter_name": "Length", "specification": "282 mm"},
        {"product_id": 59, "parameter_name": "Width", "specification": "117mm"},
        {"product_id": 59, "parameter_name": "Height", "specification": "41mm"},
        {"product_id": 59, "parameter_name": "Accessories included", "specification": "User manual"},
        {"product_id": 59, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 59, "parameter_name": "Manufacturer code", "specification": "GV-N3060GAMING OC-12GD 2.0"},
        
        {"product_id": 60, "parameter_name": "Graphics card series", "specification": "Radeon™ RX 6000"},
        {"product_id": 60, "parameter_name": "Upscaling technique", "specification": "AMD FSR 3"},
        {"product_id": 60, "parameter_name": "Graphic layout", "specification": "Radeon™ RX 6600"},
        {"product_id": 60, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16 (x8 mode)"},
        {"product_id": 60, "parameter_name": "Memory", "specification": "8GB"},
        {"product_id": 60, "parameter_name": "A type of memory", "specification": "GDDR6"},
        {"product_id": 60, "parameter_name": "Memory bus", "specification": "128 bit"},
        {"product_id": 60, "parameter_name": "Efficient memory clocking", "specification": "14000MHz"},
        {"product_id": 60, "parameter_name": "Core clock in boost mode", "specification": "2491MHz (2044 MHz Gaming Mode)"},
        {"product_id": 60, "parameter_name": "Stream Processors", "specification": "1792"},
        {"product_id": 60, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 60, "parameter_name": "Number of fans", "specification": "3"},
        {"product_id": 60, "parameter_name": "Backlight", "specification": "NO"},
        {"product_id": 60, "parameter_name": "Types of outputs", "specification": "HDMI 2.1 - 2 pcs.DisplayPort 1.4 - 2 pcs."},
        {"product_id": 60, "parameter_name": "Supported libraries", "specification": "DirectX 12OpenGL 4.6"},
        {"product_id": 60, "parameter_name": "Power connector", "specification": "8 pin - 1 pc."},
        {"product_id": 60, "parameter_name": "Recommended power supply power", "specification": "500W"},
        {"product_id": 60, "parameter_name": "Length", "specification": "282 mm"},
        {"product_id": 60, "parameter_name": "Width", "specification": "113mm"},
        {"product_id": 60, "parameter_name": "Height", "specification": "41mm"},
        {"product_id": 60, "parameter_name": "PCB format", "specification": "ATX"},
        {"product_id": 60, "parameter_name": "Number of occupied slots", "specification": "Dual slot"},
        {"product_id": 60, "parameter_name": "Accessories included", "specification": "User manual"},
        {"product_id": 60, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 60, "parameter_name": "Producent code", "specification": "GV-R66EAGLE-8GD"},

        {"product_id": 61, "parameter_name": "Graphics card series", "specification": "GeForce RTX 40 series"},
        {"product_id": 61, "parameter_name": "Ray tracing support", "specification": "Yes"},
        {"product_id": 61, "parameter_name": "Upscaling technique", "specification": "Nvidia DLSS 3.5"},
        {"product_id": 61, "parameter_name": "Graphic layout", "specification": "GeForce RTX 4060 Ti"},
        {"product_id": 61, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16 (x8 mode)"},
        {"product_id": 61, "parameter_name": "Memory", "specification": "16GB"},
        {"product_id": 61, "parameter_name": "A type of memory", "specification": "GDDR6"},
        {"product_id": 61, "parameter_name": "Memory bus", "specification": "128 bit"},
        {"product_id": 61, "parameter_name": "Core clock in boost mode", "specification": "2610MHz (2625 MHz OC Mode)"},
        {"product_id": 61, "parameter_name": "CUDA cores", "specification": "4352"},
        {"product_id": 61, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 61, "parameter_name": "Number of fans", "specification": "2"},
        {"product_id": 61, "parameter_name": "Backlight", "specification": "NO"},
        {"product_id": 61, "parameter_name": "Types of outputs", "specification": "HDMI 2.1a - 1 pc.DisplayPort 1.4a - 3 pcs."},
        {"product_id": 61, "parameter_name": "Number of monitors supported", "specification": "4"},
        {"product_id": 61, "parameter_name": "Supported libraries", "specification": "DirectX 12 UltimateOpenGL 4.6"},
        {"product_id": 61, "parameter_name": "Power connector", "specification": "8 pin - 1 pc."},
        {"product_id": 61, "parameter_name": "Recommended power supply power", "specification": "550 W"},
        {"product_id": 61, "parameter_name": "Power consumption", "specification": "165 W"},
        {"product_id": 61, "parameter_name": "Length", "specification": "199mm"},
        {"product_id": 61, "parameter_name": "Width", "specification": "120mm"},
        {"product_id": 61, "parameter_name": "Height", "specification": "42mm"},
        {"product_id": 61, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 61, "parameter_name": "Producent code", "specification": "RTX 4060 Ti VENTUS 2X BLACK 16G OC"},
        
        {"product_id": 62, "parameter_name": "Graphics card series", "specification": "GeForce RTX 40 series"},
        {"product_id": 62, "parameter_name": "Ray tracing support", "specification": "Yes"},
        {"product_id": 62, "parameter_name": "Upscaling technique", "specification": "Nvidia DLSS 3.5"},
        {"product_id": 62, "parameter_name": "Graphic layout", "specification": "GeForce RTX 4070 Great"},
        {"product_id": 62, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16"},
        {"product_id": 62, "parameter_name": "Memory", "specification": "12GB"},
        {"product_id": 62, "parameter_name": "A type of memory", "specification": "GDDR6X"},
        {"product_id": 62, "parameter_name": "Memory bus", "specification": "192 bit"},
        {"product_id": 62, "parameter_name": "Efficient memory clocking", "specification": "21000MHz"},
        {"product_id": 62, "parameter_name": "CUDA cores", "specification": "7168"},
        {"product_id": 62, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 62, "parameter_name": "Number of fans", "specification": "3"},
        {"product_id": 62, "parameter_name": "Backlight", "specification": "NO"},
        {"product_id": 62, "parameter_name": "Types of outputs", "specification": "HDMI 2.1 - 1 pc.DisplayPort 1.4 - 3 pcs."},
        {"product_id": 62, "parameter_name": "Number of monitors supported", "specification": "4"},
        {"product_id": 62, "parameter_name": "Supported libraries", "specification": "DirectX 12 UltimateOpenGL 4.6"},
        {"product_id": 62, "parameter_name": "Power connector", "specification": "16 pin - 1 pc."},
        {"product_id": 62, "parameter_name": "Recommended power supply power", "specification": "700 W"},
        {"product_id": 62, "parameter_name": "Length", "specification": "261 mm"},
        {"product_id": 62, "parameter_name": "Width", "specification": "126 mm"},
        {"product_id": 62, "parameter_name": "Height", "specification": "50mm"},
        {"product_id": 62, "parameter_name": "PCB format", "specification": "ATX"},
        {"product_id": 62, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 62, "parameter_name": "Producent code", "specification": "GV-N407SWF3OC-12GD"},
        
        {"product_id": 63, "parameter_name": "Graphics card series", "specification": "GeForce RTX 40 series"},
        {"product_id": 63, "parameter_name": "Ray tracing support", "specification": "Yes"},
        {"product_id": 63, "parameter_name": "Upscaling technique", "specification": "Nvidia DLSS 3.5"},
        {"product_id": 63, "parameter_name": "Graphic layout", "specification": "GeForce RTX 4070 Ti Super"},
        {"product_id": 63, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16"},
        {"product_id": 63, "parameter_name": "Memory", "specification": "16GB"},
        {"product_id": 63, "parameter_name": "A type of memory", "specification": "GDDR6X"},
        {"product_id": 63, "parameter_name": "Memory bus", "specification": "256 bit"},
        {"product_id": 63, "parameter_name": "Efficient memory clocking", "specification": "21000MHz"},
        {"product_id": 63, "parameter_name": "Core clock in boost mode", "specification": "2640MHz2655 MHz OC Mode"},
        {"product_id": 63, "parameter_name": "CUDA cores", "specification": "8448"},
        {"product_id": 63, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 63, "parameter_name": "Number of fans", "specification": "2"},
        {"product_id": 63, "parameter_name": "Backlight", "specification": "NO"},
        {"product_id": 63, "parameter_name": "Types of outputs", "specification": "HDMI 2.1a - 1 pc.DisplayPort 1.4a - 3 pcs."},
        {"product_id": 63, "parameter_name": "Number of monitors supported", "specification": "4"},
        {"product_id": 63, "parameter_name": "Supported libraries", "specification": "DirectX 12 UltimateOpenGL 4.6"},
        {"product_id": 63, "parameter_name": "Power connector", "specification": "16 pin - 1 pc."},
        {"product_id": 63, "parameter_name": "Power consumption", "specification": "285 W"},
        {"product_id": 63, "parameter_name": "Length", "specification": "242 mm"},
        {"product_id": 63, "parameter_name": "Width", "specification": "125 mm"},
        {"product_id": 63, "parameter_name": "Height", "specification": "51mm"},
        {"product_id": 63, "parameter_name": "PCB format", "specification": "ATX"},
        {"product_id": 63, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 63, "parameter_name": "Producent code", "specification": "RTX 4070 Ti SUPER 16G VENTUS 2X OC"},
        
        {"product_id": 64, "parameter_name": "Graphics card series", "specification": "GeForce RTX 40 series"},
        {"product_id": 64, "parameter_name": "Ray tracing support", "specification": "Yes"},
        {"product_id": 64, "parameter_name": "Upscaling technique", "specification": "Nvidia DLSS 3.5"},
        {"product_id": 64, "parameter_name": "Graphic layout", "specification": "GeForce RTX 4080 Super"},
        {"product_id": 64, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16"},
        {"product_id": 64, "parameter_name": "Memory", "specification": "16GB"},
        {"product_id": 64, "parameter_name": "A type of memory", "specification": "GDDR6X"},
        {"product_id": 64, "parameter_name": "Memory bus", "specification": "256 bit"},
        {"product_id": 64, "parameter_name": "Memory bandwidth", "specification": "736GB/s"},
        {"product_id": 64, "parameter_name": "Efficient memory clocking", "specification": "23000MHz"},
        {"product_id": 64, "parameter_name": "Core clock", "specification": "2295MHz"},
        {"product_id": 64, "parameter_name": "Core clock in boost mode", "specification": "2580MHz"},
        {"product_id": 64, "parameter_name": "CUDA cores", "specification": "10240"},
        {"product_id": 64, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 64, "parameter_name": "Number of fans", "specification": "3"},
        {"product_id": 64, "parameter_name": "Backlight", "specification": "NO"},
        {"product_id": 64, "parameter_name": "Types of outputs", "specification": "HDMI 2.1a - 1 pc.DisplayPort 1.4a - 3 pcs."},
        {"product_id": 64, "parameter_name": "Number of monitors supported", "specification": "4"},
        {"product_id": 64, "parameter_name": "Supported libraries", "specification": "DirectX 12 UltimateOpenGL 4.6Vulkan 1.3"},
        {"product_id": 64, "parameter_name": "Power connector", "specification": "16 pin - 1 pc."},
        {"product_id": 64, "parameter_name": "Recommended power supply power", "specification": "850 W"},
        {"product_id": 64, "parameter_name": "Power consumption", "specification": "320 W"},
        {"product_id": 64, "parameter_name": "Length", "specification": "329mm"},
        {"product_id": 64, "parameter_name": "Width", "specification": "128mm"},
        {"product_id": 64, "parameter_name": "Height", "specification": "64mm"},
        {"product_id": 64, "parameter_name": "Number of occupied slots", "specification": "3.1 slot"},
        {"product_id": 64, "parameter_name": "Accessories included", "specification": "Power cable"},
        {"product_id": 64, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 64, "parameter_name": "Producent code", "specification": "471056224-4403"},
        
        {"product_id": 65, "parameter_name": "Graphics card series", "specification": "Radeon™ RX 7000"},
        {"product_id": 65, "parameter_name": "Ray tracing support", "specification": "Yes"},
        {"product_id": 65, "parameter_name": "Upscaling technique", "specification": "AMD FSR 3"},
        {"product_id": 65, "parameter_name": "Graphic layout", "specification": "Radeon™ RX 7800 XT"},
        {"product_id": 65, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16"},
        {"product_id": 65, "parameter_name": "Memory", "specification": "16GB"},
        {"product_id": 65, "parameter_name": "A type of memory", "specification": "GDDR6"},
        {"product_id": 65, "parameter_name": "Memory bus", "specification": "256 bit"},
        {"product_id": 65, "parameter_name": "Efficient memory clocking", "specification": "19500MHz"},
        {"product_id": 65, "parameter_name": "Core clock", "specification": "2169MHz"},
        {"product_id": 65, "parameter_name": "Core clock in boost mode", "specification": "2475MHz"},
        {"product_id": 65, "parameter_name": "Stream Processors", "specification": "3840"},
        {"product_id": 65, "parameter_name": "Cooling type", "specification": "Active"},
        {"product_id": 65, "parameter_name": "Number of fans", "specification": "3"},
        {"product_id": 65, "parameter_name": "Backlight", "specification": "NO"},
        {"product_id": 65, "parameter_name": "Types of outputs", "specification": "HDMI 2.1 - 1 pc.DisplayPort 2.1 - 3 pcs."},
        {"product_id": 65, "parameter_name": "Number of monitors supported", "specification": "4"},
        {"product_id": 65, "parameter_name": "Supported libraries", "specification": "DirectX 12 UltimateOpenGL 4.6"},
        {"product_id": 65, "parameter_name": "Power connector", "specification": "8 pin - 2 pcs."},
        {"product_id": 65, "parameter_name": "Recommended power supply power", "specification": "700 W"},
        {"product_id": 65, "parameter_name": "Power consumption", "specification": "270 W"},
        {"product_id": 65, "parameter_name": "Length", "specification": "320mm"},
        {"product_id": 65, "parameter_name": "Width", "specification": "129 mm"},
        {"product_id": 65, "parameter_name": "Height", "specification": "53mm"},
        {"product_id": 65, "parameter_name": "PCB format", "specification": "ATX"},
        {"product_id": 65, "parameter_name": "Number of occupied slots", "specification": "2.5 slots"},
        {"product_id": 65, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 65, "parameter_name": "Producent code", "specification": "11330-03-20G"},

        {"product_id": 66, "parameter_name": "Graphics card series", "specification": "GeForce RTX 40 series"},
        {"product_id": 66, "parameter_name": "Ray tracing support", "specification": "Yes"},
        {"product_id": 66, "parameter_name": "Upscaling technique", "specification": "Nvidia DLSS 3.5"},
        {"product_id": 66, "parameter_name": "Graphic layout", "specification": "GeForce RTX 4090"},
        {"product_id": 66, "parameter_name": "Connector type", "specification": "PCIe 4.0 x16"},
        {"product_id": 66, "parameter_name": "Memory", "specification": "24GB"},
        {"product_id": 66, "parameter_name": "A type of memory", "specification": "GDDR6X"},
        {"product_id": 66, "parameter_name": "Memory bus", "specification": "384 bit"},
        {"product_id": 66, "parameter_name": "Efficient memory clocking", "specification": "21000MHz"},
        {"product_id": 66, "parameter_name": "Core clock in boost mode", "specification": "2520MHz (2550MHz OC Mode)"},
        {"product_id": 66, "parameter_name": "CUDA cores", "specification": "16384"},
        {"product_id": 66, "parameter_name": "Number of fans", "specification": "3"},
        {"product_id": 66, "parameter_name": "Backlight", "specification": "Yes"},
        {"product_id": 66, "parameter_name": "Types of outputs", "specification": "HDMI 2.1a - 2 pcs.DisplayPort 1.4a - 3 pcs."},
        {"product_id": 66, "parameter_name": "Number of monitors supported", "specification": "4"},
        {"product_id": 66, "parameter_name": "Supported libraries", "specification": "DirectX 12 UltimateOpenGL 4.6"},
        {"product_id": 66, "parameter_name": "Power connector", "specification": "16 pin - 1 pc."},
        {"product_id": 66, "parameter_name": "Recommended power supply power", "specification": "1000W"},
        {"product_id": 66, "parameter_name": "Length", "specification": "358 mm"},
        {"product_id": 66, "parameter_name": "Width", "specification": "149mm"},
        {"product_id": 66, "parameter_name": "Height", "specification": "70mm"},
        {"product_id": 66, "parameter_name": "PCB format", "specification": "ATX"},
        {"product_id": 66, "parameter_name": "Number of occupied slots", "specification": "3.5 slots"},
        {"product_id": 66, "parameter_name": "Accessories included", "specification": "BracketPCIe 16pin to 4x 8pin adapterROG Ring"},
        {"product_id": 66, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 66, "parameter_name": "Manufacturer code", "specification": "ROG-STRIX-RTX4090-24G-WHITE"},
        
        {"product_id": 67, "parameter_name": "Series", "specification": "Ares RGB"},
        {"product_id": 67, "parameter_name": "A type of memory", "specification": "DDR5"},
        {"product_id": 67, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 67, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 67, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 67, "parameter_name": "Timing", "specification": "7200MHz (PC5-57600)"},
        {"product_id": 67, "parameter_name": "Delays (cycle latency)", "specification": "CL 34"},
        {"product_id": 67, "parameter_name": "Timings", "specification": "CL34-42-42-84"},
        {"product_id": 67, "parameter_name": "Voltage", "specification": "1.4V"},
        {"product_id": 67, "parameter_name": "Supported OC profiles", "specification": "AMD EXPOIntel XMP"},
        {"product_id": 67, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 67, "parameter_name": "Height with cooling", "specification": "79mm"},
        {"product_id": 67, "parameter_name": "ECC memory", "specification": "Yes"},
        {"product_id": 67, "parameter_name": "Memory backlight", "specification": "Yes"},
        {"product_id": 67, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 67, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 67, "parameter_name": "Manufacturer code", "specification": "LD5U16G72C34LA-RGD"},
        
        {"product_id": 68, "parameter_name": "Series", "specification": "Beast"},
        {"product_id": 68, "parameter_name": "A type of memory", "specification": "DDR5"},
        {"product_id": 68, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 68, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 68, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 68, "parameter_name": "Timing", "specification": "5600MHz"},
        {"product_id": 68, "parameter_name": "Delays (cycle latency)", "specification": "CL 36"},
        {"product_id": 68, "parameter_name": "Timings", "specification": "CL36-38-38"},
        {"product_id": 68, "parameter_name": "Voltage", "specification": "1.25V"},
        {"product_id": 68, "parameter_name": "Supported OC profiles", "specification": "AMD EXPOIntel XMP"},
        {"product_id": 68, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 68, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 68, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 68, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 68, "parameter_name": "Manufacturer code", "specification": "KF556C36BBEK2-32"},
        
        {"product_id": 69, "parameter_name": "Series", "specification": "IRDM PRO"},
        {"product_id": 69, "parameter_name": "A type of memory", "specification": "DDR4"},
        {"product_id": 69, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 69, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 69, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 69, "parameter_name": "Timing", "specification": "3600MHz (PC4-28800)"},
        {"product_id": 69, "parameter_name": "Delays (cycle latency)", "specification": "CL 18"},
        {"product_id": 69, "parameter_name": "Timings", "specification": "CL18-22-22"},
        {"product_id": 69, "parameter_name": "Voltage", "specification": "1.35V"},
        {"product_id": 69, "parameter_name": "Supported OC profiles", "specification": "Intel XMP"},
        {"product_id": 69, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 69, "parameter_name": "ECC memory", "specification": "No"},
        {"product_id": 69, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 69, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 69, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 69, "parameter_name": "Manufacturer code", "specification": "IRP-K3600D4V64L18/32GDC"},
        
        {"product_id": 70, "parameter_name": "Series", "specification": "Viper Venom"},
        {"product_id": 70, "parameter_name": "A type of memory", "specification": "DDR5"},
        {"product_id": 70, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 70, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 70, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 70, "parameter_name": "Timing", "specification": "6000MHz (PC5-48000)"},
        {"product_id": 70, "parameter_name": "Delays (cycle latency)", "specification": "CL 36"},
        {"product_id": 70, "parameter_name": "Voltage", "specification": "1.35V"},
        {"product_id": 70, "parameter_name": "Supported OC profiles", "specification": "Intel XMP"},
        {"product_id": 70, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 70, "parameter_name": "ECC memory", "specification": "No"},
        {"product_id": 70, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 70, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 70, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 70, "parameter_name": "Manufacturer code", "specification": "PVV532G600C36K"},

        {"product_id": 71, "parameter_name": "A type of memory", "specification": "DDR4"},
        {"product_id": 71, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 71, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 71, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 71, "parameter_name": "Timing", "specification": "3200MHz (PC4-25600)"},
        {"product_id": 71, "parameter_name": "Delays (cycle latency)", "specification": "CL 16"},
        {"product_id": 71, "parameter_name": "Timings", "specification": "CL16-18-18-38"},
        {"product_id": 71, "parameter_name": "Voltage", "specification": "1.35V"},
        {"product_id": 71, "parameter_name": "Supported OC profiles", "specification": "Intel XMP"},
        {"product_id": 71, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 71, "parameter_name": "Height with cooling", "specification": "35.2mm"},
        {"product_id": 71, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 71, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 71, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 71, "parameter_name": "Manufacturer code", "specification": "LD4BU016G-R3200GDXG"},
        
        {"product_id": 72, "parameter_name": "Series", "specification": "Renegade"},
        {"product_id": 72, "parameter_name": "A type of memory", "specification": "DDR4"},
        {"product_id": 72, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 72, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 72, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 72, "parameter_name": "Timing", "specification": "3600MHz (PC4-28800)"},
        {"product_id": 72, "parameter_name": "Delays (cycle latency)", "specification": "CL16"},
        {"product_id": 72, "parameter_name": "Timings", "specification": "CL16-20-20"},
        {"product_id": 72, "parameter_name": "Voltage", "specification": "1.35V"},
        {"product_id": 72, "parameter_name": "Supported OC profiles", "specification": "Intel XMP"},
        {"product_id": 72, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 72, "parameter_name": "ECC memory", "specification": "No"},
        {"product_id": 72, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 72, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 72, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 72, "parameter_name": "Manufacturer code", "specification": "KF436C16RB12K2/32"},
        
        {"product_id": 73, "parameter_name": "Series", "specification": "Thor"},
        {"product_id": 73, "parameter_name": "A type of memory", "specification": "DDR4"},
        {"product_id": 73, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 73, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 73, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 73, "parameter_name": "Timing", "specification": "3600MHz"},
        {"product_id": 73, "parameter_name": "Delays (cycle latency)", "specification": "CL18"},
        {"product_id": 73, "parameter_name": "Timings", "specification": "CL18-22-22-42"},
        {"product_id": 73, "parameter_name": "Voltage", "specification": "1.35V"},
        {"product_id": 73, "parameter_name": "Supported OC profiles", "specification": "Intel XMP"},
        {"product_id": 73, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 73, "parameter_name": "ECC memory", "specification": "No"},
        {"product_id": 73, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 73, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 73, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 73, "parameter_name": "Manufacturer code", "specification": "LD4U16G36C18LG-RGD"},
        
        {"product_id": 74, "parameter_name": "Series", "specification": "Viper Venom"},
        {"product_id": 74, "parameter_name": "A type of memory", "specification": "DDR5"},
        {"product_id": 74, "parameter_name": "Total capacity", "specification": "64GB (2x32GB)"},
        {"product_id": 74, "parameter_name": "Module capacity", "specification": "32GB"},
        {"product_id": 74, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 74, "parameter_name": "Timing", "specification": "6000MHz"},
        {"product_id": 74, "parameter_name": "Delays (cycle latency)", "specification": "CL36"},
        {"product_id": 74, "parameter_name": "Voltage", "specification": "1.35V"},
        {"product_id": 74, "parameter_name": "Supported OC profiles", "specification": "Intel XMP"},
        {"product_id": 74, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 74, "parameter_name": "ECC memory", "specification": "No"},
        {"product_id": 74, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 74, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 74, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 74, "parameter_name": "Manufacturer code", "specification": "PVV564G600C36K"},
        
        {"product_id": 75, "parameter_name": "Series", "specification": "Renegade"},
        {"product_id": 75, "parameter_name": "A type of memory", "specification": "DDR4"},
        {"product_id": 75, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 75, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 75, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 75, "parameter_name": "Timing", "specification": "3600MHz (PC4-28800)"},
        {"product_id": 75, "parameter_name": "Delays (cycle latency)", "specification": "CL16"},
        {"product_id": 75, "parameter_name": "Timings", "specification": "CL16-20-20"},
        {"product_id": 75, "parameter_name": "Voltage", "specification": "1.35V"},
        {"product_id": 75, "parameter_name": "Supported OC profiles", "specification": "Intel XMP"},
        {"product_id": 75, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 75, "parameter_name": "ECC memory", "specification": "No"},
        {"product_id": 75, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 75, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 75, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 75, "parameter_name": "Manufacturer code", "specification": "KF436C16RB12K2/32"},

        {"product_id": 76, "parameter_name": "Series", "specification": "Viper Steel"},
        {"product_id": 76, "parameter_name": "A type of memory", "specification": "DDR4"},
        {"product_id": 76, "parameter_name": "Total capacity", "specification": "32GB (2x16GB)"},
        {"product_id": 76, "parameter_name": "Module capacity", "specification": "16GB"},
        {"product_id": 76, "parameter_name": "Number of modules", "specification": "2"},
        {"product_id": 76, "parameter_name": "Timing", "specification": "3600MHz"},
        {"product_id": 76, "parameter_name": "Delays (cycle latency)", "specification": "CL18"},
        {"product_id": 76, "parameter_name": "Timings", "specification": "CL18-22-22-42"},
        {"product_id": 76, "parameter_name": "Voltage", "specification": "1.35V"},
        {"product_id": 76, "parameter_name": "Supported OC profiles", "specification": "Intel XMP"},
        {"product_id": 76, "parameter_name": "Cooling", "specification": "Radiator"},
        {"product_id": 76, "parameter_name": "ECC memory", "specification": "No"},
        {"product_id": 76, "parameter_name": "Memory backlight", "specification": "No"},
        {"product_id": 76, "parameter_name": "Color", "specification": "Gray"},
        {"product_id": 76, "parameter_name": "Guarantee", "specification": "Lifetime (manufacturers warranty)"},
        {"product_id": 76, "parameter_name": "Manufacturer code", "specification": "PVS432G360C8K"},
        
        {"product_id": 77, "parameter_name": "Chipset Cooling Type", "specification": "Passive"},
        {"product_id": 77, "parameter_name": "Supported Processor Families", "specification": "AMD Ryzen™"},
        {"product_id": 77, "parameter_name": "Processor Socket", "specification": "Socket AM5"},
        {"product_id": 77, "parameter_name": "Chipset", "specification": "AMD B650"},
        {"product_id": 77, "parameter_name": "Processor Architecture", "specification": "Zen 4 (5th Generation)"},
        {"product_id": 77, "parameter_name": "Supported Memory Type", "specification": "DDR5-5200 MHzDDR5-4800 MHzDDR5-4400 MHz"},
        {"product_id": 77, "parameter_name": "Supported Memory Type (OC)", "specification": "DDR5-6400 MHzDDR5-6200 MHzDDR5-6000 MHzDDR5-5600  MHz"},
        {"product_id": 77, "parameter_name": "Number of Memory Slots", "specification": "4 x DIMM"},
        {"product_id": 77, "parameter_name": "Maximum RAM Size", "specification": "128 GB"},
        {"product_id": 77, "parameter_name": "Memory Architecture", "specification": "Dual-channel"},
        {"product_id": 77, "parameter_name": "Internal Connectors", "specification": "SATA III (6 Gb/s) - 4M.2 PCIe NVMe 4.0 x4 - 2PCIe  4.0 x16 - 1PCIe 3.0 x1 - 1USB 3.2 Gen. 2 Type-C  - 1USB 3.2 Gen. 1 - 1USB 2.0 - 2ARGB 3-pin  Connector - 1RGB 4-pin Connector - 1COM  Connector - 1Front Panel Audio - 1CPU Fan  Connector 4-pin - 1SYS/CHA Fan Connector - 38-pin  Power Connector - 124-pin Power Connector - 1TPM  Module Connector - 1"},
        {"product_id": 77, "parameter_name": "External Connectors", "specification": "HDMI - 1DisplayPort - 2RJ45 (LAN) 2.5 Gbps -  1USB Type-C - 1USB 3.2 Gen. 1 - 2USB 3.2  Gen. 2 - 1USB 2.0 - 4PS/2 Keyboard/Mouse - 1Audio  Jack - 3Wi-Fi Antenna Connector - 2Q-Flash Plus  Button - 1"},
        {"product_id": 77, "parameter_name": "RAID Support", "specification": "RAID 0RAID 1RAID 10"},
        {"product_id": 77, "parameter_name": "Multi-GPU Support", "specification": "No"},
        {"product_id": 77, "parameter_name": "Integrated Graphics Support", "specification": "Yes"},
        {"product_id": 77, "parameter_name": "Wireless Connectivity", "specification": "Wi-Fi 6E (802.11 a/b/g/n/ac/ax)Bluetooth"},
        {"product_id": 77, "parameter_name": "Additional Features", "specification": "LED Lighting"},
        {"product_id": 77, "parameter_name": "Form Factor", "specification": "mATX"},
        {"product_id": 77, "parameter_name": "Width", "specification": "244 mm"},
        {"product_id": 77, "parameter_name": "Height", "specification": "244 mm"},
        {"product_id": 77, "parameter_name": "Accessories Included", "specification": "User ManualWi-Fi 2.4/5 GHz Antenna - 1SATA Cable  - 2Mounting Screws"},
        {"product_id": 77, "parameter_name": "Color", "specification": "Brown-Gray"},
        {"product_id": 77, "parameter_name": "Warranty", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 77, "parameter_name": "Manufacturer Code", "specification": "[SSDPR-CX400-02T-G2]"},
        
        {"product_id": 78, "parameter_name": "Motherboard Chipset Cooling Type", "specification": "Passive"},
        {"product_id": 78, "parameter_name": "Supported Processor Families", "specification": "AMD Ryzen™"},
        {"product_id": 78, "parameter_name": "CPU Socket", "specification": "Socket AM5"},
        {"product_id": 78, "parameter_name": "Chipset", "specification": "AMD B650"},
        {"product_id": 78, "parameter_name": "Processor Architecture", "specification": "Zen 4 (5th Generation)"},
        {"product_id": 78, "parameter_name": "Number of Memory Banks", "specification": "4 x DIMMs"},
        {"product_id": 78, "parameter_name": "Maximum RAM Size", "specification": "192GB"},
        {"product_id": 78, "parameter_name": "Memory Architecture", "specification": "Dual-channel"},
        {"product_id": 78, "parameter_name": "Internal Connectors", "specification": "SATA III (6 Gb/s) - 6 pcs.M.2 PCIe NVMe 4.0 x4 - 3 pcs.  PCIe 4.0 x16 - 2 pcs.  PCIe 3.0 x1 - 1 pc.  Front Panel Audio  CPU Fan Connector 4 Pin - 1 pc.  SYS/CHA Fan Connector - 5 pcs.  AIO Pump Connector - 1 pc.  Power Connector 8 Pin - 2 pcs.  24 Pin Power Connector - 1 pc."},
        {"product_id": 78, "parameter_name": "External Connectors", "specification": "VGA (D-Sub) - 1 pc.  HDMI - 1 pc.  DisplayPort - 1 pc.  RJ45 (LAN) 2.5 Gbps - 1 pc.  USB Type-C - 1 pc.  USB 3.2 Gen. 1 - 2  pcs.  USB 3.2 Gen. 2 - 1 pc.  USB 2.0 - 4 pcs.PS/2  keyboard/mouse - 1 pc.Audio jack - 6 pcs.Wi-Fi  antenna connector - 2 pcs.Flash BIOS Button - 1 pc."},
        {"product_id": 78, "parameter_name": "RAID Support", "specification": "RAID 0RAID 1RAID 5RAID 10"},
        {"product_id": 78, "parameter_name": "Multiple Graphics Card Support", "specification": "AMD CrossFireX"},
        {"product_id": 78, "parameter_name": "Support for Graphics Chips in Processors", "specification": "Yes"},
        {"product_id": 78, "parameter_name": "Wireless Connectivity", "specification": "Wi-Fi 6E (802.11 a/b/g/n/ac/ax)Bluetooth"},
        {"product_id": 78, "parameter_name": "Format", "specification": "ATX"},
        {"product_id": 78, "parameter_name": "Accessories Included", "specification": "User ManualWi-Fi Antenna 2.4/5 GHz - 2 pcs.SATA  Cable - 1 pc.Fitting Elements"},
        {"product_id": 78, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 78, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        
        {"product_id": 79, "parameter_name": "Construction of Power Supply Section", "specification": "8"},
        {"product_id": 79, "parameter_name": "Cooling of Power Supply Section", "specification": "Yes (Partially cooled power section with aluminum heatsink)"},
        {"product_id": 79, "parameter_name": "Compatible with M.2 SSDs with Heatsink", "specification": "Yes - no collision"},
        {"product_id": 79, "parameter_name": "Motherboard Chipset Cooling Type", "specification": "Passive"},
        {"product_id": 79, "parameter_name": "Supported Processor Families", "specification": "Intel Core i9  Intel Core i7  Intel Core i5  Intel Core i3Intel CeleronIntel Pentium"},
        {"product_id": 79, "parameter_name": "CPU Socket", "specification": "Socket 1700"},
        {"product_id": 79, "parameter_name": "Chipset", "specification": "Intel B660"},
        {"product_id": 79, "parameter_name": "Processor Architecture", "specification": "Alder Lake-S (12th Generation)  Raptor Lake (13th  generation)"},
        {"product_id": 79, "parameter_name": "Type of Memory Supported", "specification": "DDR4-3200MHz  DDR4-3000MHz  DDR4-2933MHz  DDR4-2800MHz  DDR4-2666MHz  DDR4-2400MHz  DDR4-2133MHz"},
        {"product_id": 79, "parameter_name": "Type of Supported OC Memory", "specification": "DDR4-5000MHzDDR4-4800MHzDDR4-4600MHzDDR4-4400MHzDDR4-4266MHzDDR4-4000MHzDDR4-3733MHzDDR4-3600MHzDDR4-3466MHzDDR4-3400MHzDDR4-3333MHz"},
        {"product_id": 79, "parameter_name": "Number of Memory Banks", "specification": "4 x DIMMs"},
        {"product_id": 79, "parameter_name": "Maximum RAM Size", "specification": "128 GB"},
        {"product_id": 79, "parameter_name": "Memory Architecture", "specification": "Dual-channel"},
        {"product_id": 79, "parameter_name": "Internal Connectors", "specification": "SATA III (6 Gb/s) - 4 pcs.  M.2 PCIe NVMe 4.0 x4 - 2 pcs.  PCIe  4.0 x16 - 1PCIe 3.0 x1 - 1USB  3.2 Gen. 2 Type-C - 1 pc.USB 3.2 Gen. 1 - 1 pc.USB  2.0 - 2 pcs.ARGB 3 pin connector - 3 pcs.RGB 4 pin connector - 2 pcs.COM connector - 1 pc.Front Panel AudioCPU fan  connector 4 pin - 1 pc.SYS/CHA fan connector - 3 pcs.AIO pump connector - 1 pc.Power connector 8  pin - 1 pc.24 pin power connector - 1 pc.TPM  module connector - 1 pc.Thunderbolt 4 - 1 pc."},
        {"product_id": 79, "parameter_name": "External Connectors", "specification": "VGA (D-Sub) - 1 pc.HDMI - 1 pc.DisplayPort - 1 pc.RJ45 (LAN) 2.5  Gbps - 1 pc.USB Type-C - 1 pc.USB 3.2 Gen. 1 - 2  pcs.USB 3.2 Gen. 2 - 1 pc.USB 2.0 - 4 pcs.PS/2  keyboard/mouse - 1 pc.Audio jack - 6 pcs.Wi-Fi  antenna connector - 2 pcs.Flash BIOS Button - 1 pc."},
        {"product_id": 79, "parameter_name": "RAID Support", "specification": "RAID 0RAID 1RAID 5RAID 10"},
        {"product_id": 79, "parameter_name": "Multiple Graphics Card Support", "specification": "AMD CrossFireX"},
        {"product_id": 79, "parameter_name": "Support for Graphics Chips", "specification": "Yes"},
        {"product_id": 79, "parameter_name": "Wireless connectivity", "specification": "NO"},
        {"product_id": 79, "parameter_name": "Additional Information", "specification": "Compatibility with Raptor Lake processors requires a BIOS/UEFI update"},
        {"product_id": 79, "parameter_name": "Format", "specification": "ATX"},
        {"product_id": 79, "parameter_name": "Width", "specification": "244mm"},
        {"product_id": 79, "parameter_name": "Height", "specification": "305mm"},
        {"product_id": 79, "parameter_name": "Accessories Included", "specification": "User manualDisc with driversWi-Fi antenna 2.4/5  GHz - 1 pc.SATA cable - 2 pcs."},
        {"product_id": 79, "parameter_name": "Color", "specification": "Black and silver"},
        {"product_id": 79, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        
        {"product_id": 80, "parameter_name": "Motherboard chipset cooling type", "specification": "Passive"},
        {"product_id": 80, "parameter_name": "Supported processor families", "specification": "Intel Core i9Intel Core i7Intel Core i5Intel  Core i3Intel CeleronIntel Pentium"},
        {"product_id": 80, "parameter_name": "CPU socket", "specification": "Socket 1700"},
        {"product_id": 80, "parameter_name": "Chipset", "specification": "Intel Z790"},
        {"product_id": 80, "parameter_name": "Processor architecture", "specification": "Alder Lake-S (12th generation)Raptor Lake (13th  generation)Raptor Lake Refresh (14th generation)"},
        {"product_id": 80, "parameter_name": "Type of memory supported", "specification": "DDR5-5600MHzDDR5-5400MHzDDR5-5200MHzDDR5-5000MHzDDR5-4800MHz"},
        {"product_id": 80, "parameter_name": "Type of supported OC memory", "specification": "DDR5-7200MHzDDR5-7000MHzDDR5-6800MHzDDR5-6600MHzDDR5-6400MHzDDR5-6200MHzDDR5-6000MHzDDR5-5800MHz"},
        {"product_id": 80, "parameter_name": "Number of memory banks", "specification": "4 x DIMMs"},
        {"product_id": 80, "parameter_name": "Maximum RAM size", "specification": "256GB"},
        {"product_id": 80, "parameter_name": "Memory architecture", "specification": "Dual-channel"},
        {"product_id": 80, "parameter_name": "Internal connectors", "specification": "SATA III (6 Gb/s) - 6 pcs.M.2 PCIe NVMe 4.0 x4 / SATA  - 2 pcs.M.2 PCIe NVMe 4.0 x4 - 2 pcs.PCIe 5.0  x16 - 1 pc.PCIe 4.0 x16 (x4 mode) - 1 pc.PCIe  3.0 x16 (x1 mode) - 1 pc.PCIe 3.0 x1 - 1 pc.USB  3.2 Gen. 2 Type-C - 1 pc.USB 3.2 Gen. 1 - 2 pcs.USB  2.0 - 2 pcs.ARGB 3 pin connector - 2 pcs.RGB 4  pin connector - 1 pc.Front Panel AudioCPU fan  connector 4 pin - 1 pc.SYS/CHA fan connector - 6  pcs.AIO pump connector - 1 pc.Power connector 8  pin - 2 pcs.24 pin power connector - 1 pc.TPM  module connector - 1 pc.Thunderbolt 4 - 1 pc."},
        {"product_id": 80, "parameter_name": "External connectors", "specification": "HDMI - 1 pc.DisplayPort - 1 pc.RJ45 (LAN) 2.5  Gbps - 1 pc.USB Type-C - 1 pc.USB 3.2 Gen. 1 - 2  pcs.USB 3.2 Gen. 2 - 1 pc.USB 2.0 - 4 pcs.PS/2  keyboard/mouse - 1 pc.Audio jack - 6 pcs.Wi-Fi  antenna connector - 2 pcs.Flash BIOS Button - 1 pc."},
        {"product_id": 80, "parameter_name": "RAID support", "specification": "RAID 0RAID 1RAID 5RAID 10"},
        {"product_id": 80, "parameter_name": "Multiple graphics card support", "specification": "AMD CrossFireX"},
        {"product_id": 80, "parameter_name": "Support for graphics chips", "specification": "Yes"},
        {"product_id": 80, "parameter_name": "Wireless connectivity", "specification": "Wi-Fi 6E (802.11 a/b/g/n/ac/ax)Bluetooth"},
        {"product_id": 80, "parameter_name": "Format", "specification": "ATX"},
        {"product_id": 80, "parameter_name": "Width", "specification": "244mm"},
        {"product_id": 80, "parameter_name": "Height", "specification": "305mm"},
        {"product_id": 80, "parameter_name": "Accessories included", "specification": "User manualDisc with driversWi-Fi antenna 2.4/5  GHz - 1 pc.SATA cable - 2 pcs."},
        {"product_id": 80, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 80, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},

        {"product_id": 81, "parameter_name": "Construction of the power supply", "specification": "12+1"},
        {"product_id": 81, "parameter_name": "Cooling of the power supply section", "specification": "Yes (Fully cooled power section with aluminum heatsink)"},
        {"product_id": 81, "parameter_name": "Motherboard chipset cooling type", "specification": "Passive"},
        {"product_id": 81, "parameter_name": "Supported processor families", "specification": "Intel Core i9Intel Core i7Intel Core i5Intel  Core i3Intel CeleronIntel Pentium"},
        {"product_id": 81, "parameter_name": "CPU socket", "specification": "Socket 1700"},
        {"product_id": 81, "parameter_name": "Chipset", "specification": "Intel B760"},
        {"product_id": 81, "parameter_name": "Processor architecture", "specification": "Alder Lake-S (12th generation)Raptor Lake (13th  generation)"},
        {"product_id": 81, "parameter_name": "Type of memory supported", "specification": "DDR4-3200MHzDDR4-3000MHzDDR4-2933MHzDDR4-2800MHzDDR4-2666MHzDDR4-2400MHzDDR4-2133MHz"},
        {"product_id": 81, "parameter_name": "Type of supported OC memory", "specification": "DDR4-5333MHzDDR4-5066MHzDDR4-5000MHzDDR4-4800MHzDDR4-4600MHzDDR4-4400MHzDDR4-4266MHzDDR4-4000MHzDDR4-3733MHzDDR4-3600MHzDDR4-3466MHzDDR4-3400MHzDDR4-3333MHz"},
        {"product_id": 81, "parameter_name": "Number of memory banks", "specification": "4 x DIMMs"},
        {"product_id": 81, "parameter_name": "Maximum RAM size", "specification": "128GB"},
        {"product_id": 81, "parameter_name": "Memory architecture", "specification": "Dual-channel"},
        {"product_id": 81, "parameter_name": "Internal connectors", "specification": "SATA III (6 Gb/s) - 4M.2 PCIe NVMe 4.0 x4 - 3  pcs.PCIe 5.0 x16 - 1 pc.PCIe 3.0 x16 (x4 mode) -  1 pc.PCIe 3.0 x1 - 1 pc.USB 3.2 Gen. 2 Type-C -  1 pc.USB 3.2 Gen. 1 - 1 pc.USB 2.0 - 2 pcs.ARGB  3 pin connector - 3 pcs.RGB 4 pin connector - 1 pc.COM  Connector - 1 pc.Front Panel Audio - CPU fan  Connector 4-pin - 2 pcs.SYS/CHA fan Connector - 4  pcs.AIO pump Connector - 1 pc.4 pin power  Connector - 1 pc.Power Connector 8 pin - 1 pc.24  pin power Connector - 1 pc.Thunderbolt 4 - 1 pc."},
        {"product_id": 81, "parameter_name": "External connectors", "specification": "HDMI - 1 pc.DisplayPort - 1 pc.RJ45 (LAN) 2.5  Gbps - 1 pc.USB Type-C - 1 pc.USB 3.2 Gen. 1 - 3  pcs.USB 3.2 Gen.  2 - 2 pcs.USB 2.0 - 1 pc.Audio  jack - 5 pcs.S/PDIF  - 1 pc.Q-Flash Plus button - 1 pc."},
        {"product_id": 81, "parameter_name": "RAID support", "specification": "RAID 0RAID 1RAID 10"},
        {"product_id": 81, "parameter_name": "Multiple graphics card support", "specification": "AMD CrossFireX"},
        {"product_id": 81, "parameter_name": "Support for graphics chips", "specification": "Yes"},
        {"product_id": 81, "parameter_name": "Audio system", "specification": "Realtek HD audio"},
        {"product_id": 81, "parameter_name": "Wireless connectivity", "specification": "Wi-Fi 6 (802.11 a/b/g/n/ac/ax)Bluetooth"},
        {"product_id": 81, "parameter_name": "Additional information", "specification": "LED backlight"},
        {"product_id": 81, "parameter_name": "Format", "specification": "ATX"},
        {"product_id": 81, "parameter_name": "Width", "specification": "244 mm"},
        {"product_id": 81, "parameter_name": "Height", "specification": "305 mm"},
        {"product_id": 81, "parameter_name": "Accessories included", "specification": "User manualWi-Fi antenna 2.4/5 GHz - 1 pc.SATA  cable - 2 pcs.Fitting elements"},
        {"product_id": 81, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 81, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        
        {"product_id": 82, "parameter_name": "Construction of the power supply", "specification": "10+2+1"},
        {"product_id": 82, "parameter_name": "Cooling of the power supply section", "specification": "Yes (Fully cooled power section with aluminum heatsink)"},
        {"product_id": 82, "parameter_name": "Motherboard chipset cooling type", "specification": "Passive"},
        {"product_id": 82, "parameter_name": "Supported processor families", "specification": "AMD Ryzen™"},
        {"product_id": 82, "parameter_name": "CPU socket", "specification": "Socket AM4"},
        {"product_id": 82, "parameter_name": "Chipset", "specification": "AMD B550"},
        {"product_id": 82, "parameter_name": "Processor architecture", "specification": "Zen 2 (3rd generation)Zen 3 (4th generation)"},
        {"product_id": 82, "parameter_name": "Type of memory supported", "specification": "DDR4-3200MHzDDR4-3066MHzDDR4-3000MHzDDR4-2933MHzDDR4-2800MHzDDR4-2666MHzDDR4-2400MHzDDR4-2133MHzDDR4-1866MHz"},
        {"product_id": 82, "parameter_name": "Type of supported OC memory", "specification": "DDR4-5100MHzDDR4-5000MHzDDR4-4866MHzDDR4-4800MHzDDR4-4733MHzDDR4-4600MHzDDR4-4533MHzDDR4-4400MHzDDR4-4266MHzDDR4-4133MHzDDR4-4000MHzDDR4-3866MHzDDR4-3733MHzDDR4-3600MHzDDR4-3466MHzDDR4-3200MHzDDR4-3066MHzDDR4-3000MHzDDR4-2933MHzDDR4-2800MHzDDR4-2666MHz"},
        {"product_id": 82, "parameter_name": "Number of memory banks", "specification": "4 x DIMMs"},
        {"product_id": 82, "parameter_name": "Maximum RAM size", "specification": "128 GB"},
        {"product_id": 82, "parameter_name": "Memory architecture", "specification": "Dual-channel"},
        {"product_id": 82, "parameter_name": "Internal connectors", "specification": "SATA III (6 Gb/s) - 6 pcs.M.2 PCIe NVMe 4.0 x4 - 3 pcs.PCIe 4.0 x16 - 2 pcs.PCIe 3.0 x1 - 1 pc.Front Panel Audio - CPU Fan Connector 4 Pin - 1 pc.SYS/CHA Fan Connector - 5 pcs.AIO Pump Connector - 1 pc.Power Connector 8 Pin - 2 pcs.24 Pin Power Connector - 1 pc."},
        {"product_id": 82, "parameter_name": "External connectors", "specification": "HDMI - 1 pc.DisplayPort - 1 pc.RJ45 (LAN) - 1  pc.USB 3.2 Gen. 1 - 4 pcs.USB 2.0 - 4 pcs.PS/2  keyboard/mouse - 1 pc.Audio jack - 6 pcs.RAID  support"},
        {"product_id": 82, "parameter_name": "RAID support", "specification": "RAID 0RAID 1RAID 10"},
        {"product_id": 82, "parameter_name": "Multiple graphics card support", "specification": "AMD CrossFireX"},
        
        {"product_id": 83, "parameter_name": "Construction of the power supply", "specification": "8+2"},
        {"product_id": 83, "parameter_name": "Cooling of the power supply section", "specification": "Yes (Fully cooled power section with aluminum heatsink)"},
        {"product_id": 83, "parameter_name": "Compatible with m.2 SSDs", "specification": "Yes - no collision"},
        {"product_id": 83, "parameter_name": "Motherboard chipset cooling type", "specification": "Passive"},
        {"product_id": 83, "parameter_name": "Supported processor families", "specification": "AMD Ryzen™"},
        {"product_id": 83, "parameter_name": "CPU socket", "specification": "Socket AM4"},
        {"product_id": 83, "parameter_name": "Chipset", "specification": "AMD B450"},
        {"product_id": 83, "parameter_name": "Processor architecture", "specification": "Zen (1st generation)Zen+ (2nd generation)Zen 2  (3rd generation)Zen 3 (4th generation)"},
        {"product_id": 83, "parameter_name": "Type of memory supported", "specification": "DDR4-2933MHzDDR4-2666MHzDDR4-2400MHzDDR4-2133MHz"},
        {"product_id": 83, "parameter_name": "Type of supported OC memory", "specification": "DDR4-3600MHzDDR4-3466MHzDDR4-3200MHz"},
        {"product_id": 83, "parameter_name": "Number of memory banks", "specification": "4 x DIMMs"},
        {"product_id": 83, "parameter_name": "Maximum RAM size", "specification": "128 GB"},
        {"product_id": 83, "parameter_name": "Memory architecture", "specification": "Dual-channel"},
        {"product_id": 83, "parameter_name": "Internal connectors", "specification": "SATA III (6 Gb/s) - 6 pcs.M.2 PCIe NVMe 3.0 x4 / SATA  - 1 pc.M.2 PCIe NVMe 3.0 x2 - 1 pc.PCIe 3.0 x16  - 1 pc.PCIe 3.0 x16 (x4 mode) - 1 pc.PCIe 3.0 x1 - 1 pc.USB 3.2 Gen. 1 - 1 pc.USB 2.0 - 2  pcs.ARGB 3 pin connector - 2 pcs.RGB 4 pin connector - 1 pc.COM connector - 1 pc.Front  Panel Audio - S/PDIF output connector - 1 pc.CPU  fan connector 4 pin - 1 pc.SYS/CHA fan connector - 3  pcs.Power connector 8 pin - 1 pc.24 pin power connector - 1 pc.TPM module connector - 1 pc."},
        {"product_id": 83, "parameter_name": "External connectors", "specification": "HDMI - 1 pc.DisplayPort - 1 pc.RJ45 (LAN) - 1  pc.USB 3.2 Gen. 1 - 4 pcs.USB 2.0 - 4 pcs.PS/2  keyboard/mouse - 1 pc.Audio jack - 6 pcs.RAID  support"},
        {"product_id": 83, "parameter_name": "RAID support", "specification": "RAID 0RAID 1RAID 10"},
        {"product_id": 83, "parameter_name": "Multiple graphics card support", "specification": "AMD CrossFireX"},
        
        {"product_id": 84, "parameter_name": "Supported processor families", "specification": "AMD Ryzen™"},
        {"product_id": 84, "parameter_name": "CPU socket", "specification": "Socket AM4"},
        {"product_id": 84, "parameter_name": "Chipset", "specification": "AMD B550"},
        {"product_id": 84, "parameter_name": "Processor architecture", "specification": "Zen 2 (3rd generation)Zen 3 (4th generation)"},
        {"product_id": 84, "parameter_name": "Type of memory supported", "specification": "DDR4-3200MHzDDR4-3000MHzDDR4-2800MHzDDR4-2666MHzDDR4-2400MHzDDR4-2133MHz"},
        {"product_id": 84, "parameter_name": "Type of supported OC memory", "specification": "DDR4-5100MHzDDR4-4800MHzDDR4-4600MHzDDR4-4400MHzDDR4-4133MHzDDR4-4000MHzDDR4-3866MHzDDR4-3600MHzDDR4-3466MHz"},
        {"product_id": 84, "parameter_name": "Number of memory banks", "specification": "4 x DIMMs"},
        {"product_id": 84, "parameter_name": "Maximum RAM size", "specification": "128GB"},
        {"product_id": 84, "parameter_name": "Memory architecture", "specification": "Dual-channel"},
        {"product_id": 84, "parameter_name": "Internal connectors", "specification": "SATA III (6 Gb/s) - 6 pcs.M.2 PCIe NVMe 3.0 x4 / SATA  - 1 pc.M.2 PCIe NVMe 4.0 x4 / SATA - 1 pc.PCIe  4.0/3.0 x16 - 1 pc.PCIe 3.0 x16 (x4 mode) - 1 pc.PCIe  3.0 x1 - 3 pcs.USB 3.2 Gen. 1 - 1 pc.USB 2.0 - 2  pcs.ARGB 3 pin connector - 1 pc.RGB 4 pin  connector - 2 pcs."},
        {"product_id": 84, "parameter_name": "Front Panel Audio", "specification": "CPU fan connector 4 pin - 2 pcs.SYS/CHA fan connector -  3 pcs.AIO pump connector - 1 pc.4 pin power  connector - 1 pc.Power connector 8 pin - 1 pc.24 pin power connector - 1 pc.Temperature sensor - 1  pc.Thunderbolt 3 - 1 pc."},
        {"product_id": 84, "parameter_name": "External connectors", "specification": "HDMI - 1 pc.DisplayPort - 1 pc.RJ45 (LAN) 2.5  Gbps - 1 pc.USB Type-C - 1 pc.USB 3.2 Gen. 1 - 4  pcs.USB 3.2 Gen. 2 - 1 pc.USB 2.0 - 2 pcs.Audio jack - 5 pcs.S/PDIF - 1 pc.Flash BIOS Button - 1  pc."},
        {"product_id": 84, "parameter_name": "RAID support", "specification": "RAID 0RAID 1RAID 10"},
        {"product_id": 84, "parameter_name": "Multiple graphics card support", "specification": "AMD CrossFireX"},
        {"product_id": 84, "parameter_name": "Support for graphics chips", "specification": "Yes"},
        {"product_id": 84, "parameter_name": "Audio system", "specification": "ROG SupremeFX"},
        {"product_id": 84, "parameter_name": "Wireless connectivity", "specification": "NO"},
        {"product_id": 84, "parameter_name": "Additional information", "specification": "LED backlightNot compatible with AMD Ryzen 5 3400G and  AMD Ryzen 3 3200G"},
        {"product_id": 84, "parameter_name": "Format", "specification": "ATX"},
        {"product_id": 84, "parameter_name": "Width", "specification": "245mm"},
        {"product_id": 84, "parameter_name": "Height", "specification": "306mm"},
        {"product_id": 84, "parameter_name": "Accessories included", "specification": "User manualDisc with driversSATA cable - 4  pcs.M.2 mounting elements - 1 pc.Extension for  ARGB - 1 pc"},
        {"product_id": 84, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 84, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 84, "parameter_name": "Manufacturer code", "specification": "90MB14S0-M0EAY0"},
        
        {"product_id": 85, "parameter_name": "Construction of the power supply", "specification": "12+2"},
        {"product_id": 85, "parameter_name": "Cooling of the power supply section", "specification": "Yes (Fully cooled power section with aluminum heatsink)"},
        {"product_id": 85, "parameter_name": "Compatible with m.2 SSDs", "specification": "Yes - no collision"},
        {"product_id": 85, "parameter_name": "Motherboard chipset cooling", "specification": "Passive"},
        {"product_id": 85, "parameter_name": "Supported processor families", "specification": "AMD Ryzen™"},
        {"product_id": 85, "parameter_name": "CPU socket", "specification": "Socket AM4"},
        {"product_id": 85, "parameter_name": "Chipset", "specification": "AMD B550"},
        {"product_id": 85, "parameter_name": "Processor architecture", "specification": "Zen 2 (3rd generation)Zen 3 (4th generation)"},
        {"product_id": 85, "parameter_name": "Type of memory supported", "specification": "DDR4-3200MHzDDR4-2933MHzDDR4-2666MHzDDR4-2400MHzDDR4-2133MHz"},
        {"product_id": 85, "parameter_name": "Type of supported OC memory", "specification": "DDR4-4733MHzDDR4-4600MHzDDR4-4400MHzDDR4-4000MHzDDR4-3600MHzDDR4-3333MHz"},
        {"product_id": 85, "parameter_name": "Number of memory banks", "specification": "4 x DIMMs"},
        {"product_id": 85, "parameter_name": "Maximum RAM size", "specification": "128GB"},
        {"product_id": 85, "parameter_name": "Memory architecture", "specification": "Dual-channel"},
        {"product_id": 85, "parameter_name": "Internal connectors", "specification": "SATA III (6 Gb/s) - 4 pcs.M.2 PCIe NVMe 3.0 x4 / SATA  - 1 pc.M.2 PCIe NVMe 4.0 x4 / SATA - 1 pc.PCIe  4.0 x16 - 1 pc.PCIe 3.0 x16 (x2 mode) - 1 pc.PCIe  3.0 x16 (x1 mode) - 1 pc.PCIe 3.0 x1 - 1 pc.USB  3.2 Gen. 1 Type-C - 1 pc.USB 3.2 Gen. 1 - 1 pc.USB  2.0 - 2 pcs.ARGB 3 pin connector - 2 pcs.RGB 4  pin connector - 2 pcs."},
        {"product_id": 85, "parameter_name": "Front Panel Audio", "specification": "CPU fan connector 4 pin - 1 pc.SYS/CHA fan connector -  3 pcs.AIO pump connector - 1 pc.Power connector  8 pin - 1 pc.24 pin power connector - 1 pc.TPM module connector - 1 pc."},
        {"product_id": 85, "parameter_name": "External connectors", "specification": "HDMI - 1 pc.DisplayPort - 1 pc.RJ45 (LAN) 2.5  Gbps - 1 pc.USB 3.2 Gen. 1 - 3 pcs.USB 3.2 Gen.  2 - 2 pcs.USB 2.0 - 2 pcs.Audio jack - 5 pcs.S/PDIF  - 1 pc.Q-Flash Plus button - 1 pc."},
        {"product_id": 85, "parameter_name": "RAID support", "specification": "RAID 0RAID 1RAID 10"},
        {"product_id": 85, "parameter_name": "Multiple graphics card support", "specification": "AMD CrossFireX"},
        {"product_id": 85, "parameter_name": "Support for graphics chips", "specification": "Yes"},
        {"product_id": 85, "parameter_name": "Audio system", "specification": "Realtek ALC1200"},
        {"product_id": 85, "parameter_name": "Wireless connectivity", "specification": "NO"},
        {"product_id": 85, "parameter_name": "Additional information", "specification": "Not compatible with AMD Ryzen 5 3400G and AMD Ryzen 3 3200G"},
        {"product_id": 85, "parameter_name": "Format", "specification": "ATX"},

        {"product_id": 86, "parameter_name": "Construction of the power supply", "specification": "12+2"},
        {"product_id": 86, "parameter_name": "Cooling of the power supply section", "specification": "Yes (Fully cooled power section with aluminum heatsink)"},
        {"product_id": 86, "parameter_name": "Compatible with m.2 SSDs with ", "specification": "Yes - no collision"},
        {"product_id": 86, "parameter_name": "Motherboard chipset cooling", "specification": "Passive"},
        {"product_id": 86, "parameter_name": "Supported processor", "specification": "AMD Ryzen™"},
        {"product_id": 86, "parameter_name": "CPU socket", "specification": "Socket AM4"},
        {"product_id": 86, "parameter_name": "Chipset", "specification": "AMD B550"},
        {"product_id": 86, "parameter_name": "Processor architecture", "specification": "Zen 2 (3rd generation)Zen 3 (4th generation)"},
        {"product_id": 86, "parameter_name": "Type of memory supported", "specification": "DDR4-3200MHzDDR4-2933MHzDDR4-2666MHzDDR4-2400MHzDDR4-2133MHz"},
        {"product_id": 86, "parameter_name": "Type of supported OC", "specification": "DDR4-4733MHzDDR4-4600MHzDDR4-4400MHzDDR4-4000MHzDDR4-3600MHzDDR4-3333MHz"},
        {"product_id": 86, "parameter_name": "Number of memory banks", "specification": "4 x DIMMs"},
        {"product_id": 86, "parameter_name": "Maximum RAM size", "specification": "128GB"},
        {"product_id": 86, "parameter_name": "Memory architecture", "specification": "Dual-channel"},
        {"product_id": 86, "parameter_name": "Internal connectors", "specification": "SATA III (6 Gb/s) - 4 pcs.  M.2 PCIe NVMe 3.0 x4 / SATA - 1 pc.  M.2 PCIe NVMe 4.0 x4 / SATA - 1 pc.  PCIe 4.0 x16 - 1 pc.  PCIe 3.0 x16 (x2 mode) - 1 pc.  PCIe 3.0 x16 (x1 mode) - 1 pc.  PCIe 3.0 x1 - 1 pc.  USB 3.2 Gen. 1 Type-C - 1 pc.  USB 3.2 Gen. 1 - 1 pc.  USB 2.0 - 2 pcs.  ARGB 3 pin connector - 2 pcs.  RGB 4 pin connector - 2 pcs."},
        {"product_id": 86, "parameter_name": "Front Panel Audio", "specification": "CPU fan connector 4 pin - 1 pc.  SYS/CHA fan connector - 3 pcs.  AIO pump connector - 1 pc.  Power connector 8 pin - 1 pc.  24 pin power connector - 1 pc.  TPM module connector - 1 pc."},
        {"product_id": 86, "parameter_name": "External connectors", "specification": "HDMI - 1 pc.  DisplayPort - 1 pc.  RJ45 (LAN) 2.5 Gbps - 1 pc.  USB 3.2 Gen. 1 - 3 pcs.  USB 3.2 Gen. 2 - 2 pcs.  USB 2.0 - 2 pcs.  Audio jack - 5 pcs.  S/PDIF - 1 pc.  Q-Flash Plus button - 1 pc."},
        {"product_id": 86, "parameter_name": "RAID support", "specification": "RAID 0RAID 1RAID 10"},
        {"product_id": 86, "parameter_name": "Multiple graphics card", "specification": "AMD CrossFireX"},
        {"product_id": 86, "parameter_name": "Support for graphics chips", "specification": "Yes"},
        {"product_id": 86, "parameter_name": "Audio system", "specification": "Realtek ALC1200"},
        {"product_id": 86, "parameter_name": "Wireless connectivity", "specification": "NO"},
        {"product_id": 86, "parameter_name": "Additional information", "specification": "Not compatible with AMD Ryzen 5 3400G and AMD Ryzen 3 3200G"},
        {"product_id": 86, "parameter_name": "Format", "specification": "ATX"},
        {"product_id": 86, "parameter_name": "Width", "specification": "244 mm"},
        {"product_id": 86, "parameter_name": "Height", "specification": "305 mm"},
        {"product_id": 86, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 86, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        
        {"product_id": 87, "parameter_name": "Maximum power", "specification": "650 W"},
        {"product_id": 87, "parameter_name": "Standard", "specification": "ATX"},
        {"product_id": 87, "parameter_name": "Lead-out connectors", "specification": "CPU 4+4 (8) pin - 1 pc.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 2 pcs.  MOLEX 4-pin - 2 pcs.  SATA - 5 pcs.  FDD - 1 pc."},
        {"product_id": 87, "parameter_name": "Efficiency", "specification": "85% at 230V and 20-100% load."},
        {"product_id": 87, "parameter_name": "Certificate", "specification": "80 PLUS Bronze"},
        {"product_id": 87, "parameter_name": "Security", "specification": "Over Current Protection (OCP)  Anti-overload protection (OPP)  Thermal (OTP)  Overvoltage protection (OVP)  Short circuit protection (SCP)"},
        {"product_id": 87, "parameter_name": "PFC (power factor)", "specification": "Active"},
        {"product_id": 87, "parameter_name": "Wiring type", "specification": "Non-modular"},
        {"product_id": 87, "parameter_name": "Fan diameter", "specification": "120mm"},
        {"product_id": 87, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 87, "parameter_name": "Accessories included", "specification": "Fitting elements"},
        {"product_id": 87, "parameter_name": "Height", "specification": "86mm"},
        {"product_id": 87, "parameter_name": "Width", "specification": "150mm"},
        {"product_id": 87, "parameter_name": "Depth", "specification": "140mm"},
        {"product_id": 87, "parameter_name": "Guarantee", "specification": "60 months (manufacturers warranty)"},
        {"product_id": 87, "parameter_name": "Manufacturer code", "specification": "MAG A650BN"},
        
        {"product_id": 88, "parameter_name": "Maximum power", "specification": "1000W"},
        {"product_id": 88, "parameter_name": "Standard", "specification": "ATX"},
        {"product_id": 88, "parameter_name": "Lead-out connectors", "specification": "CPU 4+4 (8) pin - 2 pcs.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 6 pcs.  MOLEX 4-pin - 5 pcs.  SATA - 14 pcs.  FDD - 1 pc."},
        {"product_id": 88, "parameter_name": "Efficiency", "specification": "94-96% at 230V and 20-100% load"},
        {"product_id": 88, "parameter_name": "Certificate", "specification": "80 PLUS Titanium"},
        {"product_id": 88, "parameter_name": "Security", "specification": "Over Current Protection (OCP)  Anti-overload protection (OPP)  Thermal (OTP)  Overvoltage protection (OVP)  Short circuit protection (SCP)  Against undervoltage (UVP)"},
        {"product_id": 88, "parameter_name": "PFC (power factor)", "specification": "Active"},
        {"product_id": 88, "parameter_name": "Wiring type", "specification": "Modular"},
        {"product_id": 88, "parameter_name": "Fan diameter", "specification": "135mm"},
        {"product_id": 88, "parameter_name": "Accessories included", "specification": "Fitting elements"},
        {"product_id": 88, "parameter_name": "Height", "specification": "87mm"},
        {"product_id": 88, "parameter_name": "Width", "specification": "140mm"},
        {"product_id": 88, "parameter_name": "Depth", "specification": "150mm"},
        {"product_id": 88, "parameter_name": "Guarantee", "specification": "84 months (manufacturers warranty)"},
        {"product_id": 88, "parameter_name": "Manufacturer code", "specification": "EY7A010"},
        
        {"product_id": 89, "parameter_name": "Maximum power", "specification": "550 W"},
        {"product_id": 89, "parameter_name": "Standard", "specification": "ATX"},
        {"product_id": 89, "parameter_name": "Lead-out connectors", "specification": "CPU 4+4 (8) pin - 1 pc.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 2 pcs.  MOLEX 4-pin - 4 pcs.  SATA - 5 pcs.  FDD - 1 pc."},
        {"product_id": 89, "parameter_name": "Efficiency", "specification": "85% at 230V and 20-100% load"},
        {"product_id": 89, "parameter_name": "Certificate", "specification": "Not certified"},
        {"product_id": 89, "parameter_name": "PFC (power factor)", "specification": "Active"},
        {"product_id": 89, "parameter_name": "Wiring type", "specification": "Non-modular"},
        {"product_id": 89, "parameter_name": "Fan diameter", "specification": "120mm"},
        {"product_id": 89, "parameter_name": "Height", "specification": "86mm"},
        {"product_id": 89, "parameter_name": "Width", "specification": "150mm"},
        {"product_id": 89, "parameter_name": "Depth", "specification": "140mm"},
        {"product_id": 89, "parameter_name": "Guarantee", "specification": "24 months (manufacturers warranty)"},
        {"product_id": 89, "parameter_name": "Manufacturer code", "specification": "PS-LTP-0550NPCNEU-2"},
        
        {"product_id": 90, "parameter_name": "Maximum power", "specification": "1000W"},
        {"product_id": 90, "parameter_name": "Standard", "specification": "ATX"},
        {"product_id": 90, "parameter_name": "Lead-out connectors", "specification": "CPU 4+4 (8) pin - 2 pcs.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 6 pcs.  MOLEX 4-pin - 5 pcs.  SATA - 14 pcs.  FDD - 1 pc."},
        {"product_id": 90, "parameter_name": "Efficiency", "specification": "94-96% at 230V and 20-100% load"},
        {"product_id": 90, "parameter_name": "Certificate", "specification": "80 PLUS Titanium"},
        {"product_id": 90, "parameter_name": "Security", "specification": "Over Current Protection (OCP)  Anti-overload protection (OPP)  Thermal (OTP)  Overvoltage protection (OVP)  Short circuit protection (SCP)  Against undervoltage (UVP)"},
        {"product_id": 90, "parameter_name": "Wiring type", "specification": "Modular"},
        {"product_id": 90, "parameter_name": "Fan diameter", "specification": "135mm"},
        {"product_id": 90, "parameter_name": "Accessories included", "specification": "Fitting elements"},
        {"product_id": 90, "parameter_name": "Height", "specification": "86mm"},
        {"product_id": 90, "parameter_name": "Width", "specification": "150mm"},
        {"product_id": 90, "parameter_name": "Depth", "specification": "170mm"},
        {"product_id": 90, "parameter_name": "Guarantee", "specification": "144 months (manufacturers warranty)"},
        {"product_id": 90, "parameter_name": "Manufacturer code", "specification": "PRIME TX-1000"},

        {"product_id": 91, "parameter_name": "Maximum power", "specification": "750W"},
        {"product_id": 91, "parameter_name": "Standard", "specification": "SFX"},
        {"product_id": 91, "parameter_name": "Lead-out connectors", "specification": "CPU 4+4 (8) pin - 2 pcs.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 4 pcs.  MOLEX 4-pin - 3 pcs.  SATA - 6 pcs."},
        {"product_id": 91, "parameter_name": "Efficiency", "specification": "92% at 230V and 20-100% load"},
        {"product_id": 91, "parameter_name": "Certificate", "specification": "80 PLUS Platinum"},
        {"product_id": 91, "parameter_name": "Security", "specification": "Over Current Protection (OCP)  Anti-overload protection (OPP)  Thermal (OTP)  Overvoltage protection (OVP)  Short circuit protection (SCP)  Against undervoltage (UVP)"},
        {"product_id": 91, "parameter_name": "Wiring type", "specification": "Modular"},
        {"product_id": 91, "parameter_name": "Fan diameter", "specification": "92mm"},
        {"product_id": 91, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 91, "parameter_name": "Additional information", "specification": "Quiet fan operationZeroRPM mode"},
        {"product_id": 91, "parameter_name": "Accessories included", "specification": "Fitting elements"},
        {"product_id": 91, "parameter_name": "Height", "specification": "64mm"},
        {"product_id": 91, "parameter_name": "Width", "specification": "100mm"},
        {"product_id": 91, "parameter_name": "Depth", "specification": "125mm"},
        {"product_id": 91, "parameter_name": "Guarantee", "specification": "120 months (manufacturers warranty)"},
        {"product_id": 91, "parameter_name": "Manufacturer code", "specification": "FOCUS-SPX-750"},
        
        {"product_id": 92, "parameter_name": "Maximum power", "specification": "750W"},
        {"product_id": 92, "parameter_name": "Standard", "specification": "ATX"},
        {"product_id": 92, "parameter_name": "Lead-out connectors", "specification": "CPU 4+4 (8) pin - 1 pc.  CPU 8-pin - 1 pc.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 4 pcs.  MOLEX 4-pin - 4 pcs.  SATA - 12 pcs."},
        {"product_id": 92, "parameter_name": "Efficiency", "specification": "90% at 230V and 20-100% load"},
        {"product_id": 92, "parameter_name": "Certificate", "specification": "80 PLUS Gold"},
        {"product_id": 92, "parameter_name": "Security", "specification": "Over Current Protection (OCP)  Anti-overload protection (OPP)  Thermal (OTP)  Overvoltage protection (OVP)  Short circuit protection (SCP)  Against undervoltage (UVP)  PFC (power factor correction): Active"},
        {"product_id": 92, "parameter_name": "Wiring type", "specification": "Modular"},
        {"product_id": 92, "parameter_name": "Fan diameter", "specification": "120mm"},
        {"product_id": 92, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 92, "parameter_name": "Accessories included", "specification": "Fitting elements"},
        {"product_id": 92, "parameter_name": "Height", "specification": "86mm"},
        {"product_id": 92, "parameter_name": "Width", "specification": "150mm"},
        {"product_id": 92, "parameter_name": "Depth", "specification": "160mm"},
        {"product_id": 92, "parameter_name": "Guarantee", "specification": "60 months (manufacturers warranty)"},
        {"product_id": 92, "parameter_name": "Manufacturer code", "specification": "MPE-7501-AFAAG-EU"},
        
        {"product_id": 93, "parameter_name": "Maximum power", "specification": "1200W"},
        {"product_id": 93, "parameter_name": "Standard", "specification": "ATX 3.0"},
        {"product_id": 93, "parameter_name": "Lead-out connectors", "specification": "CPU 4+4 (8) pin - 1 pc.  CPU 8-pin - 1 pc.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 5.0 12+4 (16) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 2 pcs.  MOLEX 4-pin - 4 pcs.  SATA - 8 pcs."},
        {"product_id": 93, "parameter_name": "Efficiency", "specification": "87-90% at 230V and 20-100% load"},
        {"product_id": 93, "parameter_name": "Certificate", "specification": "80 PLUS Gold"},
        {"product_id": 93, "parameter_name": "PFC (power factor correction)", "specification": "Active"},
        {"product_id": 93, "parameter_name": "Wiring type", "specification": "Modular"},
        {"product_id": 93, "parameter_name": "Fan diameter", "specification": "135mm"},
        {"product_id": 93, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 93, "parameter_name": "Additional information", "specification": "ZeroRPM mode"},
        {"product_id": 93, "parameter_name": "Accessories included", "specification": "Fitting elements"},
        {"product_id": 93, "parameter_name": "Height", "specification": "86mm"},
        {"product_id": 93, "parameter_name": "Width", "specification": "150mm"},
        {"product_id": 93, "parameter_name": "Depth", "specification": "150mm"},
        {"product_id": 93, "parameter_name": "Guarantee", "specification": "120 months (manufacturers warranty)"},
        {"product_id": 93, "parameter_name": "Manufacturer code", "specification": "PA-2G1BB-EU"},
        
        {"product_id": 94, "parameter_name": "Maximum power", "specification": "850W"},
        {"product_id": 94, "parameter_name": "Standard", "specification": "ATX"},
        {"product_id": 94, "parameter_name": "Lead-out connectors", "specification": "CPU 8-pin - 2 pcs.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 3 pcs.  MOLEX 4-pin - 1 pc.  SATA - 11 pcs."},
        {"product_id": 94, "parameter_name": "Efficiency", "specification": "88-91% at 230V and 20-100% load"},
        {"product_id": 94, "parameter_name": "Certificate", "specification": "80 PLUS Gold"},
        {"product_id": 94, "parameter_name": "Security", "specification": "Over Current Protection (OCP)  Anti-overload protection (OPP)  Thermal (OTP)  Overvoltage protection (OVP)  Short circuit protection (SCP)  Against surge currents (SIP)  Against undervoltage (UVP)"},
        {"product_id": 94, "parameter_name": "PFC (power factor correction)", "specification": "Active"},
        {"product_id": 94, "parameter_name": "Wiring type", "specification": "Modular"},
        {"product_id": 94, "parameter_name": "Fan diameter", "specification": "120mm"},
        {"product_id": 94, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 94, "parameter_name": "Accessories included", "specification": "Fitting elements"},
        {"product_id": 94, "parameter_name": "Height", "specification": "87mm"},
        {"product_id": 94, "parameter_name": "Width", "specification": "140mm"},
        {"product_id": 94, "parameter_name": "Depth", "specification": "150mm"},
        {"product_id": 94, "parameter_name": "Guarantee", "specification": "60 months (manufacturers warranty)"},
        {"product_id": 94, "parameter_name": "Manufacturer code", "specification": "KRX0119"},
        
        {"product_id": 95, "parameter_name": "Maximum power", "specification": "750W"},
        {"product_id": 95, "parameter_name": "Standard", "specification": "ATX"},
        {"product_id": 95, "parameter_name": "Lead-out connectors", "specification": "CPU 4+4 (8) pin - 2 pcs.  EPS12V 20+4 (24) pin - 1 pc.  PCI-E 2.0 6+2 (8) pin - 4 pcs.  MOLEX 4-pin - 3 pcs.  SATA - 10 pcs."},
        {"product_id": 95, "parameter_name": "Efficiency", "specification": "90% at 230V and 20-100% load"},
        {"product_id": 95, "parameter_name": "Certificate", "specification": "80 PLUS Gold"},
        {"product_id": 95, "parameter_name": "Security", "specification": "Over Current Protection (OCP)  Anti-overload protection (OPP)  Thermal (OTP)  Overvoltage protection (OVP)  Short circuit protection (SCP)  Against undervoltage (UVP)"},
        {"product_id": 95, "parameter_name": "PFC (power factor correction)", "specification": "Active"},
        {"product_id": 95, "parameter_name": "Wiring type", "specification": "Modular"},
        {"product_id": 95, "parameter_name": "Fan diameter", "specification": "120mm"},
        {"product_id": 95, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 95, "parameter_name": "Additional information", "specification": "ZeroRPM mode"},
        {"product_id": 95, "parameter_name": "Accessories included", "specification": "Fitting elements"},
        {"product_id": 95, "parameter_name": "Height", "specification": "86mm"},
        {"product_id": 95, "parameter_name": "Width", "specification": "150mm"},
        {"product_id": 95, "parameter_name": "Depth", "specification": "140mm"},
        {"product_id": 95, "parameter_name": "Guarantee", "specification": "120 months (manufacturers warranty)"},
        {"product_id": 95, "parameter_name": "Manufacturer code", "specification": "FOCUS-GX-750"},

        {"product_id": 96, "parameter_name": "Processor family", "specification": "AMD Ryzen™"},
        {"product_id": 96, "parameter_name": "CPU series", "specification": "Ryzen™ 9 7900X3D"},
        {"product_id": 96, "parameter_name": "Processor socket (socket)", "specification": "Socket AM5"},
        {"product_id": 96, "parameter_name": "Supported chipset", "specification": "X670X670EB650EB650"},
        {"product_id": 96, "parameter_name": "Architecture", "specification": "Zen 4"},
        {"product_id": 96, "parameter_name": "Core clock", "specification": "4.4 GHz (5.6 GHz in turbo mode)"},
        {"product_id": 96, "parameter_name": "Number of physical cores", "specification": "12 cores"},
        {"product_id": 96, "parameter_name": "Number of threads", "specification": "24 threads"},
        {"product_id": 96, "parameter_name": "Cache", "specification": "140 MB"},
        {"product_id": 96, "parameter_name": "Integrated graphics system", "specification": "Yes"},
        {"product_id": 96, "parameter_name": "Graphics system model", "specification": "Radeon™ Graphics"},
        {"product_id": 96, "parameter_name": "Type of memory supported", "specification": "DDR5-5200"},
        {"product_id": 96, "parameter_name": "Lithographic process", "specification": "5nm"},
        {"product_id": 96, "parameter_name": "Power Consumption (TDP)", "specification": "120 W"},
        {"product_id": 96, "parameter_name": "Technologies used", "specification": "AMD 3D V-Cache™AMD EXPO™"},
        {"product_id": 96, "parameter_name": "Additional information", "specification": "BOX versionCooling included: NO"},
        {"product_id": 96, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 96, "parameter_name": "Manufacturer code", "specification": "100-100000909WOF"},

        {"product_id": 97, "parameter_name": "Processor family", "specification": "AMD Ryzen™"},
        {"product_id": 97, "parameter_name": "CPU series", "specification": "Ryzen™ 7 7800X3D"},
        {"product_id": 97, "parameter_name": "Processor socket (socket)", "specification": "Socket AM5"},
        {"product_id": 97, "parameter_name": "Supported chipset", "specification": "X670X670EB650EB650"},
        {"product_id": 97, "parameter_name": "Architecture", "specification": "Zen 4"},
        {"product_id": 97, "parameter_name": "Core clock", "specification": "4.2 GHz (5.0 GHz in turbo mode)"},
        {"product_id": 97, "parameter_name": "Number of physical cores", "specification": "8 cores"},
        {"product_id": 97, "parameter_name": "Number of threads", "specification": "16 threads"},
        {"product_id": 97, "parameter_name": "Cache", "specification": "104 MB"},
        {"product_id": 97, "parameter_name": "Integrated graphics system", "specification": "Yes"},
        {"product_id": 97, "parameter_name": "Graphics system model", "specification": "Radeon™ Graphics"},
        {"product_id": 97, "parameter_name": "Type of memory supported", "specification": "DDR5-5200"},
        {"product_id": 97, "parameter_name": "Lithographic process", "specification": "5nm"},
        {"product_id": 97, "parameter_name": "Power Consumption (TDP)", "specification": "120 W"},
        {"product_id": 97, "parameter_name": "Technologies used", "specification": "AMD 3D V-Cache™AMD EXPO™"},
        {"product_id": 97, "parameter_name": "Additional information", "specification": "BOX versionCooling included: NO"},
        {"product_id": 97, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 97, "parameter_name": "Manufacturer code", "specification": "100-100000910WOF"},

        {"product_id": 98, "parameter_name": "Processor family", "specification": "AMD Ryzen™"},
        {"product_id": 98, "parameter_name": "CPU series", "specification": "Ryzen™ 5 5600"},
        {"product_id": 98, "parameter_name": "Processor socket (socket)", "specification": "Socket AM4"},
        {"product_id": 98, "parameter_name": "Supported chipset", "specification": "A520B350B450B550X470X570X370"},
        {"product_id": 98, "parameter_name": "Architecture", "specification": "Zen 3"},
        {"product_id": 98, "parameter_name": "Core clock", "specification": "3.5 GHz (4.4 GHz in turbo mode)"},
        {"product_id": 98, "parameter_name": "Number of physical cores", "specification": "6 cores"},
        {"product_id": 98, "parameter_name": "Number of threads", "specification": "12 threads"},
        {"product_id": 98, "parameter_name": "Unlocked multiplier", "specification": "Yes"},
        {"product_id": 98, "parameter_name": "Cache", "specification": "35 MB"},
        {"product_id": 98, "parameter_name": "Integrated graphics system", "specification": "NO"},
        {"product_id": 98, "parameter_name": "Type of memory supported", "specification": "DDR4-3200 (PC4-25600)"},
        {"product_id": 98, "parameter_name": "Lithographic process", "specification": "7nm"},
        {"product_id": 98, "parameter_name": "Power Consumption (TDP)", "specification": "65 W"},
        {"product_id": 98, "parameter_name": "Additional information", "specification": "BOX versionCooling included: Yes"},
        {"product_id": 98, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 98, "parameter_name": "Manufacturer code", "specification": "100-100000927BOX"},

        {"product_id": 99, "parameter_name": "Processor family", "specification": "AMD Ryzen™"},
        {"product_id": 99, "parameter_name": "CPU series", "specification": "Ryzen™ 5 7600X"},
        {"product_id": 99, "parameter_name": "Processor socket (socket)", "specification": "Socket AM5"},
        {"product_id": 99, "parameter_name": "Supported chipset", "specification": "X670X670EB650EB650"},
        {"product_id": 99, "parameter_name": "Architecture", "specification": "Zen 4"},
        {"product_id": 99, "parameter_name": "Core clock", "specification": "4.7 GHz (5.3 GHz in turbo mode)"},
        {"product_id": 99, "parameter_name": "Number of physical cores", "specification": "6 cores"},
        {"product_id": 99, "parameter_name": "Number of threads", "specification": "12 threads"},
        {"product_id": 99, "parameter_name": "Unlocked multiplier", "specification": "Yes"},
        {"product_id": 99, "parameter_name": "Cache", "specification": "22 MB"},
        {"product_id": 99, "parameter_name": "Integrated graphics system", "specification": "Yes"},
        {"product_id": 99, "parameter_name": "Graphics system model", "specification": "Radeon™ 760M"},
        {"product_id": 99, "parameter_name": "Type of memory supported", "specification": "DDR5-5200DDR5-3600"},
        {"product_id": 99, "parameter_name": "Lithographic process", "specification": "4nm"},
        {"product_id": 99, "parameter_name": "Power Consumption (TDP)", "specification": "65 W"},
        {"product_id": 99, "parameter_name": "Technologies used", "specification": "AMD EXPO™AMD Ryzen™ AI"},
        {"product_id": 99, "parameter_name": "Additional information", "specification": "ECC memory supportBOX version"},
        {"product_id": 99, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 99, "parameter_name": "Manufacturer code", "specification": "100-100000593WOF"},

        {"product_id": 100, "parameter_name": "Processor family", "specification": "AMD Ryzen™"},
        {"product_id": 100, "parameter_name": "CPU series", "specification": "Ryzen™ 5 8600G"},
        {"product_id": 100, "parameter_name": "Processor socket (socket)", "specification": "Socket AM5"},
        {"product_id": 100, "parameter_name": "Architecture", "specification": "Zen 4"},
        {"product_id": 100, "parameter_name": "Core clock", "specification": "4.3 GHz (5.0 GHz in turbo mode)"},
        {"product_id": 100, "parameter_name": "Number of physical cores", "specification": "6 cores"},
        {"product_id": 100, "parameter_name": "Number of threads", "specification": "12 threads"},
        {"product_id": 100, "parameter_name": "Unlocked multiplier", "specification": "Yes"},
        {"product_id": 100, "parameter_name": "Cache", "specification": "22 MB"},
        {"product_id": 100, "parameter_name": "Integrated graphics system", "specification": "Yes"},
        {"product_id": 100, "parameter_name": "Graphics system model", "specification": "Radeon™ 760M"},
        {"product_id": 100, "parameter_name": "Type of memory supported", "specification": "DDR5-5200DDR5-3600"},
        {"product_id": 100, "parameter_name": "Lithographic process", "specification": "4nm"},
        {"product_id": 100, "parameter_name": "Power Consumption (TDP)", "specification": "65 W"},
        {"product_id": 100, "parameter_name": "Technologies used", "specification": "AMD EXPO™AMD Ryzen™ AI"},
        {"product_id": 100, "parameter_name": "Additional information", "specification": "BOX versionCooling included"},
        {"product_id": 100, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 100, "parameter_name": "Manufacturer code", "specification": "100-100001237BOX"},

        {"product_id": 101, "parameter_name": "Processor family", "specification": "Intel Core i5"},
        {"product_id": 101, "parameter_name": "CPU series", "specification": "i5-13400F"},
        {"product_id": 101, "parameter_name": "Processor socket (socket)", "specification": "Socket 1700"},
        {"product_id": 101, "parameter_name": "Architecture", "specification": "Raptor Lake (13th Generation)"},
        {"product_id": 101, "parameter_name": "Core clock", "specification": "2.5 GHz (4.6 GHz in turbo mode)"},
        {"product_id": 101, "parameter_name": "Number of physical cores", "specification": "10 cores"},
        {"product_id": 101, "parameter_name": "Core types", "specification": "6 Performance Cores4 Efficient cores"},
        {"product_id": 101, "parameter_name": "Number of threads", "specification": "16 threads"},
        {"product_id": 101, "parameter_name": "Unlocked multiplier", "specification": "NO"},
        {"product_id": 101, "parameter_name": "Cache", "specification": "20 MB"},
        {"product_id": 101, "parameter_name": "Integrated graphics system", "specification": "NO"},
        {"product_id": 101, "parameter_name": "Graphics system model", "specification": "Lack"},
        {"product_id": 101, "parameter_name": "Type of memory supported", "specification": "DDR5-4800DDR4-3200 (PC4-25600)"},
        {"product_id": 101, "parameter_name": "Power Consumption (TDP)", "specification": "65 W"},
        {"product_id": 101, "parameter_name": "Maximum Turbo Power (MTP)", "specification": "148 W"},
        {"product_id": 101, "parameter_name": "Additional information", "specification": "BOX versionCooling included"},
        {"product_id": 101, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 101, "parameter_name": "Manufacturer code", "specification": "BX8071513400F"},

        {"product_id": 102, "parameter_name": "Processor family", "specification": "Intel Core i9"},
        {"product_id": 102, "parameter_name": "CPU series", "specification": "i9-13900KF"},
        {"product_id": 102, "parameter_name": "Processor socket (socket)", "specification": "Socket 1700"},
        {"product_id": 102, "parameter_name": "Architecture", "specification": "Raptor Lake (13th Generation)"},
        {"product_id": 102, "parameter_name": "Core clock", "specification": "3.0 GHz (5.8 GHz in turbo mode)"},
        {"product_id": 102, "parameter_name": "Number of physical cores", "specification": "24 cores"},
        {"product_id": 102, "parameter_name": "Core types", "specification": "8 Performance Cores16 Efficient cores"},
        {"product_id": 102, "parameter_name": "Number of threads", "specification": "32 threads"},
        {"product_id": 102, "parameter_name": "Unlocked multiplier", "specification": "Yes"},
        {"product_id": 102, "parameter_name": "Cache", "specification": "36 MB"},
        {"product_id": 102, "parameter_name": "Integrated graphics system", "specification": "NO"},
        {"product_id": 102, "parameter_name": "Graphics system model", "specification": "Lack"},
        {"product_id": 102, "parameter_name": "Type of memory supported", "specification": "DDR5-5600DDR4-3200 (PC4-25600)"},
        {"product_id": 102, "parameter_name": "Lithographic process", "specification": "10nm"},
        {"product_id": 102, "parameter_name": "Power Consumption (TDP)", "specification": "125 W"},
        {"product_id": 102, "parameter_name": "Maximum Turbo Power (MTP)", "specification": "253 W"},
        {"product_id": 102, "parameter_name": "Technologies used", "specification": "Intel Turbo Boost Max 3.0"},
        {"product_id": 102, "parameter_name": "Additional information", "specification": "BOX version"},
        {"product_id": 102, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 102, "parameter_name": "Manufacturer code", "specification": "BX8071513900KF"},

        {"product_id": 103, "parameter_name": "Processor family", "specification": "Intel Core i7"},
        {"product_id": 103, "parameter_name": "CPU series", "specification": "i7-13700"},
        {"product_id": 103, "parameter_name": "Processor socket (socket)", "specification": "Socket 1700"},
        {"product_id": 103, "parameter_name": "Architecture", "specification": "Raptor Lake (13th Generation)"},
        {"product_id": 103, "parameter_name": "Core clock", "specification": "2.1 GHz (5.2 GHz in turbo mode)"},
        {"product_id": 103, "parameter_name": "Number of physical cores", "specification": "16 cores"},
        {"product_id": 103, "parameter_name": "Core types", "specification": "8 Performance Cores8 Efficient cores"},
        {"product_id": 103, "parameter_name": "Number of threads", "specification": "24 threads"},
        {"product_id": 103, "parameter_name": "Unlocked multiplier", "specification": "NO"},
        {"product_id": 103, "parameter_name": "Cache", "specification": "30 MB"},
        {"product_id": 103, "parameter_name": "Integrated graphics system", "specification": "Yes"},
        {"product_id": 103, "parameter_name": "Graphics system model", "specification": "Intel UHD Graphics 770"},
        {"product_id": 103, "parameter_name": "Type of memory supported", "specification": "DDR5-5600DDR4-3200 (PC4-25600)"},
        {"product_id": 103, "parameter_name": "Power Consumption (TDP)", "specification": "65 W"},
        {"product_id": 103, "parameter_name": "Maximum Turbo Power (MTP)", "specification": "219 W"},
        {"product_id": 103, "parameter_name": "Technologies used", "specification": "Intel Turbo Boost Max 3.0Intel® vPro™Intel®  SIPP3"},
        {"product_id": 103, "parameter_name": "Additional information", "specification": "ECC memory supportBOX version"},
        {"product_id": 103, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 103, "parameter_name": "Manufacturer code", "specification": "BX8071513700"},

        {"product_id": 104, "parameter_name": "Processor family", "specification": "Intel Core i9"},
        {"product_id": 104, "parameter_name": "CPU series", "specification": "i9-13900KF"},
        {"product_id": 104, "parameter_name": "Processor socket (socket)", "specification": "Socket 1700"},
        {"product_id": 104, "parameter_name": "Architecture", "specification": "Raptor Lake (13th Generation)"},
        {"product_id": 104, "parameter_name": "Core clock", "specification": "3.0 GHz (5.8 GHz in turbo mode)"},
        {"product_id": 104, "parameter_name": "Number of physical cores", "specification": "24 cores"},
        {"product_id": 104, "parameter_name": "Core types", "specification": "8 Performance Cores16 Efficient cores"},
        {"product_id": 104, "parameter_name": "Number of threads", "specification": "32 threads"},
        {"product_id": 104, "parameter_name": "Unlocked multiplier", "specification": "Yes"},
        {"product_id": 104, "parameter_name": "Cache", "specification": "36 MB"},
        {"product_id": 104, "parameter_name": "Integrated graphics system", "specification": "NO"},
        {"product_id": 104, "parameter_name": "Graphics system model", "specification": "Lack"},
        {"product_id": 104, "parameter_name": "Type of memory supported", "specification": "DDR5-5600DDR4-3200 (PC4-25600)"},
        {"product_id": 104, "parameter_name": "Lithographic process", "specification": "10nm"},
        {"product_id": 104, "parameter_name": "Power Consumption (TDP)", "specification": "125 W"},
        {"product_id": 104, "parameter_name": "Maximum Turbo Power (MTP)", "specification": "253 W"},
        {"product_id": 104, "parameter_name": "Technologies used", "specification": "Intel Turbo Boost Max 3.0"},
        {"product_id": 104, "parameter_name": "Additional information", "specification": "BOX version"},
        {"product_id": 104, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 104, "parameter_name": "Manufacturer code", "specification": "BX8071513900KF"},

        {"product_id": 105, "parameter_name": "Processor family", "specification": "Intel Core i3"},
        {"product_id": 105, "parameter_name": "CPU series", "specification": "i3-13100"},
        {"product_id": 105, "parameter_name": "Processor socket (socket)", "specification": "Socket 1700"},
        {"product_id": 105, "parameter_name": "Architecture", "specification": "Raptor Lake (13th Generation)"},
        {"product_id": 105, "parameter_name": "Core clock", "specification": "3.4 GHz (4.5 GHz in turbo mode)"},
        {"product_id": 105, "parameter_name": "Number of physical cores", "specification": "4 cores"},
        {"product_id": 105, "parameter_name": "Core types", "specification": "4 Performance Cores"},
        {"product_id": 105, "parameter_name": "Number of threads", "specification": "8 threads"},
        {"product_id": 105, "parameter_name": "Unlocked multiplier", "specification": "NO"},
        {"product_id": 105, "parameter_name": "Cache", "specification": "12 MB"},
        {"product_id": 105, "parameter_name": "Integrated graphics system", "specification": "Yes"},
        {"product_id": 105, "parameter_name": "Graphics system model", "specification": "Intel UHD Graphics 730"},
        {"product_id": 105, "parameter_name": "Type of memory supported", "specification": "DDR5-4800DDR4-3200 (PC4-25600)"},
        {"product_id": 105, "parameter_name": "Power Consumption (TDP)", "specification": "60 W"},
        {"product_id": 105, "parameter_name": "Maximum Turbo Power (MTP)", "specification": "89 W"},
        {"product_id": 105, "parameter_name": "Additional information", "specification": "BOX versionCooling included"},
        {"product_id": 105, "parameter_name": "Guarantee", "specification": "36 months (manufacturers warranty)"},
        {"product_id": 105, "parameter_name": "Manufacturer code", "specification": "BX8071513100"},

        {"product_id": 106, "parameter_name": "DPI", "specification": "4000 DPI"},
        {"product_id": 106, "parameter_name": "Sensor Type", "specification": "Logitech Darkfield High Precision"},
        {"product_id": 106, "parameter_name": "Wired/Wireless", "specification": "Wireless"},
        {"product_id": 106, "parameter_name": "Number of Buttons", "specification": "7 buttons"},
        {"product_id": 106, "parameter_name": "RGB Lighting", "specification": "No"},
        {"product_id": 106, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 106, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 106, "parameter_name": "Weight", "specification": "141g"},
        {"product_id": 106, "parameter_name": "Connectivity", "specification": "Bluetooth / USB Receiver"},
        {"product_id": 106, "parameter_name": "Polling Rate", "specification": "1000 Hz"},


        {"product_id": 107, "parameter_name": "DPI", "specification": "1000 DPI"},
        {"product_id": 107, "parameter_name": "Sensor Type", "specification": "Optical"},
        {"product_id": 107, "parameter_name": "Wired/Wireless", "specification": "Wireless"},
        {"product_id": 107, "parameter_name": "Number of Buttons", "specification": "5 buttons"},
        {"product_id": 107, "parameter_name": "RGB Lighting", "specification": "No"},
        {"product_id": 107, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 107, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 107, "parameter_name": "Weight", "specification": "124g"},
        {"product_id": 107, "parameter_name": "Connectivity", "specification": "USB Receiver"},
        {"product_id": 107, "parameter_name": "Battery Life", "specification": "Up to 3 years"},

        {"product_id": 108, "parameter_name": "DPI", "specification": "12,000 DPI"},
        {"product_id": 108, "parameter_name": "Sensor Type", "specification": "TrueMove3+"},
        {"product_id": 108, "parameter_name": "Wired/Wireless", "specification": "Wired"},
        {"product_id": 108, "parameter_name": "Number of Buttons", "specification": "8 buttons"},
        {"product_id": 108, "parameter_name": "RGB Lighting", "specification": "Yes"},
        {"product_id": 108, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 108, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 108, "parameter_name": "Weight", "specification": "130g"},
        {"product_id": 108, "parameter_name": "Connectivity", "specification": "USB Cable"},
        {"product_id": 108, "parameter_name": "Polling Rate", "specification": "1000 Hz"},

        {"product_id": 109, "parameter_name": "DPI", "specification": "25,600 DPI"},
        {"product_id": 109, "parameter_name": "Sensor Type", "specification": "HERO 25K"},
        {"product_id": 109, "parameter_name": "Wired/Wireless", "specification": "Wired"},
        {"product_id": 109, "parameter_name": "Number of Buttons", "specification": "11 buttons"},
        {"product_id": 109, "parameter_name": "RGB Lighting", "specification": "Yes"},
        {"product_id": 109, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 109, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 109, "parameter_name": "Weight", "specification": "121g"},
        {"product_id": 109, "parameter_name": "Connectivity", "specification": "USB Cable"},
        {"product_id": 109, "parameter_name": "Polling Rate", "specification": "1000 Hz"},

        {"product_id": 110, "parameter_name": "DPI", "specification": "16,000 DPI"},
        {"product_id": 110, "parameter_name": "Sensor Type", "specification": "Focus+ Optical Sensor"},
        {"product_id": 110, "parameter_name": "Wired/Wireless", "specification": "Wired"},
        {"product_id": 110, "parameter_name": "Number of Buttons", "specification": "11 buttons"},
        {"product_id": 110, "parameter_name": "RGB Lighting", "specification": "Yes"},
        {"product_id": 110, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 110, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 110, "parameter_name": "Weight", "specification": "125g"},
        {"product_id": 110, "parameter_name": "Connectivity", "specification": "USB Cable"},
        {"product_id": 110, "parameter_name": "Polling Rate", "specification": "1000 Hz"},

        {"product_id": 111, "parameter_name": "DPI", "specification": "8000 DPI"},
        {"product_id": 111, "parameter_name": "Sensor Type", "specification": "Optical"},
        {"product_id": 111, "parameter_name": "Wired/Wireless", "specification": "Wired"},
        {"product_id": 111, "parameter_name": "Number of Buttons", "specification": "7 buttons"},
        {"product_id": 111, "parameter_name": "RGB Lighting", "specification": "Yes"},
        {"product_id": 111, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 111, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 111, "parameter_name": "Weight", "specification": "110g"},
        {"product_id": 111, "parameter_name": "Connectivity", "specification": "USB Cable"},
        {"product_id": 111, "parameter_name": "Polling Rate", "specification": "1000 Hz"},

        {"product_id": 112, "parameter_name": "DPI", "specification": "1000 DPI"},
        {"product_id": 112, "parameter_name": "Sensor Type", "specification": "Optical"},
        {"product_id": 112, "parameter_name": "Wired/Wireless", "specification": "Wireless"},
        {"product_id": 112, "parameter_name": "Number of Buttons", "specification": "3 buttons"},
        {"product_id": 112, "parameter_name": "RGB Lighting", "specification": "No"},
        {"product_id": 112, "parameter_name": "Programmable Buttons", "specification": "No"},
        {"product_id": 112, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 112, "parameter_name": "Weight", "specification": "85g"},
        {"product_id": 112, "parameter_name": "Connectivity", "specification": "USB Receiver"},
        {"product_id": 112, "parameter_name": "Battery Life", "specification": "Up to 12 months"},

        {"product_id": 113, "parameter_name": "DPI", "specification": "8,500 DPI"},
        {"product_id": 113, "parameter_name": "Sensor Type", "specification": "TrueMove Core"},
        {"product_id": 113, "parameter_name": "Wired/Wireless", "specification": "Wired"},
        {"product_id": 113, "parameter_name": "Number of Buttons", "specification": "6 buttons"},
        {"product_id": 113, "parameter_name": "RGB Lighting", "specification": "Yes"},
        {"product_id": 113, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 113, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 113, "parameter_name": "Weight", "specification": "85g"},
        {"product_id": 113, "parameter_name": "Connectivity", "specification": "USB Cable"},
        {"product_id": 113, "parameter_name": "Polling Rate", "specification": "1000 Hz"},

        {"product_id": 114, "parameter_name": "DPI", "specification": "16,000 DPI"},
        {"product_id": 114, "parameter_name": "Sensor Type", "specification": "TrueMove Pro+"},
        {"product_id": 114, "parameter_name": "Wired/Wireless", "specification": "Wired"},
        {"product_id": 114, "parameter_name": "Number of Buttons", "specification": "8 buttons"},
        {"product_id": 114, "parameter_name": "RGB Lighting", "specification": "Yes"},
        {"product_id": 114, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 114, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 114, "parameter_name": "Weight", "specification": "130g"},
        {"product_id": 114, "parameter_name": "Connectivity", "specification": "USB Cable"},
        {"product_id": 114, "parameter_name": "Polling Rate", "specification": "1000 Hz"},

        {"product_id": 115, "parameter_name": "DPI", "specification": "20,000 DPI"},
        {"product_id": 115, "parameter_name": "Sensor Type", "specification": "Focus+ Optical Sensor"},
        {"product_id": 115, "parameter_name": "Wired/Wireless", "specification": "Wireless"},
        {"product_id": 115, "parameter_name": "Number of Buttons", "specification": "11 buttons"},
        {"product_id": 115, "parameter_name": "RGB Lighting", "specification": "Yes"},
        {"product_id": 115, "parameter_name": "Programmable Buttons", "specification": "Yes"},
        {"product_id": 115, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 115, "parameter_name": "Weight", "specification": "130g"},
        {"product_id": 115, "parameter_name": "Connectivity", "specification": "Razer HyperSpeed Wireless"},
        {"product_id": 115, "parameter_name": "Polling Rate", "specification": "1000 Hz"},

        {"product_id": 116, "parameter_name": "Connectivity", "specification": "Wireless Multi-Mode (Bluetooth/2.4GHz)"},
        {"product_id": 116, "parameter_name": "Switch Type", "specification": "Membrane"},
        {"product_id": 116, "parameter_name": "Number of Keys", "specification": "104 Keys"},
        {"product_id": 116, "parameter_name": "Backlighting", "specification": "No"},
        {"product_id": 116, "parameter_name": "Programmable Macros", "specification": "Yes"},
        {"product_id": 116, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 116, "parameter_name": "Weight", "specification": "800g"},
        {"product_id": 116, "parameter_name": "Layout", "specification": "Full-Size"},
        {"product_id": 116, "parameter_name": "Build Material", "specification": "Plastic"},
        {"product_id": 116, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 117, "parameter_name": "Connectivity", "specification": "Wired USB"},
        {"product_id": 117, "parameter_name": "Switch Type", "specification": "Mechanical Blue"},
        {"product_id": 117, "parameter_name": "Number of Keys", "specification": "87 Keys (TKL)"},
        {"product_id": 117, "parameter_name": "Backlighting", "specification": "Amber RGB"},
        {"product_id": 117, "parameter_name": "Programmable Macros", "specification": "Yes"},
        {"product_id": 117, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 117, "parameter_name": "Weight", "specification": "900g"},
        {"product_id": 117, "parameter_name": "Layout", "specification": "Tenkeyless"},
        {"product_id": 117, "parameter_name": "Build Material", "specification": "Aluminum"},
        {"product_id": 117, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 118, "parameter_name": "Connectivity", "specification": "Wired USB"},
        {"product_id": 118, "parameter_name": "Switch Type", "specification": "Hot-Swap Mechanical"},
        {"product_id": 118, "parameter_name": "Number of Keys", "specification": "87 Keys (TKL)"},
        {"product_id": 118, "parameter_name": "Backlighting", "specification": "Sapphire RGB"},
        {"product_id": 118, "parameter_name": "Programmable Macros", "specification": "Yes"},
        {"product_id": 118, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 118, "parameter_name": "Weight", "specification": "850g"},
        {"product_id": 118, "parameter_name": "Layout", "specification": "Tenkeyless"},
        {"product_id": 118, "parameter_name": "Build Material", "specification": "Aluminum"},
        {"product_id": 118, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 119, "parameter_name": "Connectivity", "specification": "Wireless USB"},
        {"product_id": 119, "parameter_name": "Switch Type", "specification": "Mechanical"},
        {"product_id": 119, "parameter_name": "Number of Keys", "specification": "104 Keys"},
        {"product_id": 119, "parameter_name": "Backlighting", "specification": "RGB"},
        {"product_id": 119, "parameter_name": "Programmable Macros", "specification": "Yes"},
        {"product_id": 119, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 119, "parameter_name": "Weight", "specification": "950g"},
        {"product_id": 119, "parameter_name": "Layout", "specification": "Full-Size"},
        {"product_id": 119, "parameter_name": "Build Material", "specification": "Steel"},
        {"product_id": 119, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 120, "parameter_name": "Connectivity", "specification": "Wireless/Bluetooth & Wired USB-C"},
        {"product_id": 120, "parameter_name": "Switch Type", "specification": "Low Profile Red Mechanical"},
        {"product_id": 120, "parameter_name": "Number of Keys", "specification": "87 Keys (TKL)"},
        {"product_id": 120, "parameter_name": "Backlighting", "specification": "RGB"},
        {"product_id": 120, "parameter_name": "Programmable Macros", "specification": "Yes"},
        {"product_id": 120, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 120, "parameter_name": "Weight", "specification": "700g"},
        {"product_id": 120, "parameter_name": "Layout", "specification": "Tenkeyless"},
        {"product_id": 120, "parameter_name": "Build Material", "specification": "Aluminum"},
        {"product_id": 120, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 121, "parameter_name": "Connectivity", "specification": "Wireless USB"},
        {"product_id": 121, "parameter_name": "Switch Type", "specification": "Mechanical"},
        {"product_id": 121, "parameter_name": "Number of Keys", "specification": "87 Keys (TKL)"},
        {"product_id": 121, "parameter_name": "Backlighting", "specification": "Sapphire RGB"},
        {"product_id": 121, "parameter_name": "Programmable Macros", "specification": "Yes"},
        {"product_id": 121, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 121, "parameter_name": "Weight", "specification": "920g"},
        {"product_id": 121, "parameter_name": "Layout", "specification": "Tenkeyless"},
        {"product_id": 121, "parameter_name": "Build Material", "specification": "Aluminum"},
        {"product_id": 121, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 122, "parameter_name": "Connectivity", "specification": "Wireless USB"},
        {"product_id": 122, "parameter_name": "Switch Type", "specification": "Membrane"},
        {"product_id": 122, "parameter_name": "Number of Keys", "specification": "104 Keys"},
        {"product_id": 122, "parameter_name": "Backlighting", "specification": "No"},
        {"product_id": 122, "parameter_name": "Programmable Macros", "specification": "No"},
        {"product_id": 122, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 122, "parameter_name": "Weight", "specification": "850g"},
        {"product_id": 122, "parameter_name": "Layout", "specification": "Full-Size"},
        {"product_id": 122, "parameter_name": "Build Material", "specification": "Plastic"},
        {"product_id": 122, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 123, "parameter_name": "Connectivity", "specification": "Wireless USB"},
        {"product_id": 123, "parameter_name": "Switch Type", "specification": "Mechanical Blue"},
        {"product_id": 123, "parameter_name": "Number of Keys", "specification": "104 Keys"},
        {"product_id": 123, "parameter_name": "Backlighting", "specification": "RGB"},
        {"product_id": 123, "parameter_name": "Programmable Macros", "specification": "Yes"},
        {"product_id": 123, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 123, "parameter_name": "Weight", "specification": "900g"},
        {"product_id": 123, "parameter_name": "Layout", "specification": "Full-Size"},
        {"product_id": 123, "parameter_name": "Build Material", "specification": "Aluminum"},
        {"product_id": 123, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 124, "parameter_name": "Connectivity", "specification": "Wired USB"},
        {"product_id": 124, "parameter_name": "Switch Type", "specification": "Quiet Membrane"},
        {"product_id": 124, "parameter_name": "Number of Keys", "specification": "104 Keys"},
        {"product_id": 124, "parameter_name": "Backlighting", "specification": "No"},
        {"product_id": 124, "parameter_name": "Programmable Macros", "specification": "No"},
        {"product_id": 124, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 124, "parameter_name": "Weight", "specification": "700g"},
        {"product_id": 124, "parameter_name": "Layout", "specification": "Full-Size"},
        {"product_id": 124, "parameter_name": "Build Material", "specification": "Plastic"},
        {"product_id": 124, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 125, "parameter_name": "Connectivity", "specification": "Wired USB"},
        {"product_id": 125, "parameter_name": "Switch Type", "specification": "OmniPoint Adjustable Mechanical Blue"},
        {"product_id": 125, "parameter_name": "Number of Keys", "specification": "87 Keys (TKL)"},
        {"product_id": 125, "parameter_name": "Backlighting", "specification": "RGB"},
        {"product_id": 125, "parameter_name": "Programmable Macros", "specification": "Yes"},
        {"product_id": 125, "parameter_name": "Ergonomic Design", "specification": "Yes"},
        {"product_id": 125, "parameter_name": "Weight", "specification": "900g"},
        {"product_id": 125, "parameter_name": "Layout", "specification": "Tenkeyless"},
        {"product_id": 125, "parameter_name": "Build Material", "specification": "Aluminum"},
        {"product_id": 125, "parameter_name": "Compatibility", "specification": "Windows/macOS"},

        {"product_id": 126, "parameter_name": "Display Size", "specification": "27-inch"},
        {"product_id": 126, "parameter_name": "Resolution", "specification": "2560x1440 (QHD)"},
        {"product_id": 126, "parameter_name": "Panel Type", "specification": "VA"},
        {"product_id": 126, "parameter_name": "Refresh Rate", "specification": "165Hz"},
        {"product_id": 126, "parameter_name": "Response Time", "specification": "1ms MPRT"},
        {"product_id": 126, "parameter_name": "Curvature", "specification": "1000R"},
        {"product_id": 126, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync Premium"},
        {"product_id": 126, "parameter_name": "Color Gamut", "specification": "100% sRGB"},
        {"product_id": 126, "parameter_name": "Connectivity", "specification": "HDMI, DisplayPort"},
        {"product_id": 126, "parameter_name": "Stand Adjustments", "specification": "Tilt, Swivel, Height"},

        {"product_id": 127, "parameter_name": "Display Size", "specification": "27-inch"},
        {"product_id": 127, "parameter_name": "Resolution", "specification": "2560x1440 (QHD)"},
        {"product_id": 127, "parameter_name": "Panel Type", "specification": "IPS"},
        {"product_id": 127, "parameter_name": "Refresh Rate", "specification": "144Hz"},
        {"product_id": 127, "parameter_name": "Response Time", "specification": "1ms"},
        {"product_id": 127, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync and NVIDIA G-SYNC Compatible"},
        {"product_id": 127, "parameter_name": "Color Gamut", "specification": "99% sRGB"},
        {"product_id": 127, "parameter_name": "Connectivity", "specification": "HDMI, DisplayPort"},
        {"product_id": 127, "parameter_name": "Stand Adjustments", "specification": "Tilt, Swivel, Height"},
        {"product_id": 127, "parameter_name": "Additional Features", "specification": "Dynamic Action Sync, Black Stabilizer"},

        {"product_id": 128, "parameter_name": "Display Size", "specification": "27-inch"},
        {"product_id": 128, "parameter_name": "Resolution", "specification": "2560x1440 (QHD)"},
        {"product_id": 128, "parameter_name": "Panel Type", "specification": "VA"},
        {"product_id": 128, "parameter_name": "Refresh Rate", "specification": "165Hz"},
        {"product_id": 128, "parameter_name": "Response Time", "specification": "1ms MPRT"},
        {"product_id": 128, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync Premium"},
        {"product_id": 128, "parameter_name": "Color Gamut", "specification": "100% sRGB"},
        {"product_id": 128, "parameter_name": "Connectivity", "specification": "HDMI, DisplayPort"},
        {"product_id": 128, "parameter_name": "Stand Adjustments", "specification": "Tilt, Swivel, Height"},
        {"product_id": 128, "parameter_name": "Design Features", "specification": "RGB Lighting, Ergonomic Stand"},

        {"product_id": 129, "parameter_name": "Display Size", "specification": "27-inch"},
        {"product_id": 129, "parameter_name": "Resolution", "specification": "2560x1440 (QHD)"},
        {"product_id": 129, "parameter_name": "Panel Type", "specification": "IPS"},
        {"product_id": 129, "parameter_name": "Refresh Rate", "specification": "165Hz"},
        {"product_id": 129, "parameter_name": "Response Time", "specification": "1ms MPRT"},
        {"product_id": 129, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync Premium"},
        {"product_id": 129, "parameter_name": "Color Gamut", "specification": "100% sRGB"},
        {"product_id": 129, "parameter_name": "Connectivity", "specification": "HDMI, DisplayPort"},
        {"product_id": 129, "parameter_name": "Stand Adjustments", "specification": "Tilt, Swivel, Height"},
        {"product_id": 129, "parameter_name": "Ergonomic Features", "specification": "Adjustable Stand, Eye Comfort Technologies"},

        {"product_id": 130, "parameter_name": "Display Size", "specification": "24-inch"},
        {"product_id": 130, "parameter_name": "Resolution", "specification": "1920x1080 (Full HD)"},
        {"product_id": 130, "parameter_name": "Panel Type", "specification": "VA"},
        {"product_id": 130, "parameter_name": "Refresh Rate", "specification": "144Hz"},
        {"product_id": 130, "parameter_name": "Response Time", "specification": "1ms MPRT"},
        {"product_id": 130, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync"},
        {"product_id": 130, "parameter_name": "Color Gamut", "specification": "100% sRGB"},
        {"product_id": 130, "parameter_name": "Connectivity", "specification": "HDMI, DisplayPort"},
        {"product_id": 130, "parameter_name": "Stand Adjustments", "specification": "Tilt, Swivel, Height"},
        {"product_id": 130, "parameter_name": "Design Features", "specification": "RGB Lighting, Curved Screen"},

        {"product_id": 131, "parameter_name": "Display Size", "specification": "27-inch"},
        {"product_id": 131, "parameter_name": "Resolution", "specification": "2560x1440 (QHD)"},
        {"product_id": 131, "parameter_name": "Panel Type", "specification": "IPS"},
        {"product_id": 131, "parameter_name": "Refresh Rate", "specification": "165Hz"},
        {"product_id": 131, "parameter_name": "Response Time", "specification": "1ms MPRT"},
        {"product_id": 131, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync Premium"},
        {"product_id": 131, "parameter_name": "Color Gamut", "specification": "100% sRGB"},
        {"product_id": 131, "parameter_name": "Connectivity", "specification": "HDMI, DisplayPort"},
        {"product_id": 131, "parameter_name": "Stand Adjustments", "specification": "Tilt, Swivel, Height"},
        {"product_id": 131, "parameter_name": "Ergonomic Design", "specification": "Adjustable Stand, Blue Light Filter"},

        {"product_id": 132, "parameter_name": "Display Size", "specification": "24-inch"},
        {"product_id": 132, "parameter_name": "Resolution", "specification": "1920x1080 (Full HD)"},
        {"product_id": 132, "parameter_name": "Panel Type", "specification": "IPS"},
        {"product_id": 132, "parameter_name": "Refresh Rate", "specification": "60Hz"},
        {"product_id": 132, "parameter_name": "Response Time", "specification": "5ms"},
        {"product_id": 132, "parameter_name": "Adaptive Sync", "specification": "N/A"},
        {"product_id": 132, "parameter_name": "Color Gamut", "specification": "72% NTSC"},
        {"product_id": 132, "parameter_name": "Connectivity", "specification": "HDMI, VGA"},
        {"product_id": 132, "parameter_name": "Stand Adjustments", "specification": "Tilt"},
        {"product_id": 132, "parameter_name": "Design Features", "specification": "Sleek Design, Flicker-Free Technology"},

        {"product_id": 133, "parameter_name": "Display Size", "specification": "27-inch"},
        {"product_id": 133, "parameter_name": "Resolution", "specification": "2560x1440 (QHD)"},
        {"product_id": 133, "parameter_name": "Panel Type", "specification": "IPS"},
        {"product_id": 133, "parameter_name": "Refresh Rate", "specification": "165Hz"},
        {"product_id": 133, "parameter_name": "Response Time", "specification": "1ms MPRT"},
        {"product_id": 133, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync Premium"},
        {"product_id": 133, "parameter_name": "Color Gamut", "specification": "95% DCI-P3"},
        {"product_id": 133, "parameter_name": "Connectivity", "specification": "HDMI, DisplayPort"},
        {"product_id": 133, "parameter_name": "Stand Adjustments", "specification": "Tilt, Swivel, Height"},
        {"product_id": 133, "parameter_name": "Design Features", "specification": "RGB Lighting, Ergonomic Stand"},

        {"product_id": 134, "parameter_name": "Display Size", "specification": "24-inch"},
        {"product_id": 134, "parameter_name": "Resolution", "specification": "1920x1080 (Full HD)"},
        {"product_id": 134, "parameter_name": "Panel Type", "specification": "IPS"},
        {"product_id": 134, "parameter_name": "Refresh Rate", "specification": "75Hz"},
        {"product_id": 134, "parameter_name": "Response Time", "specification": "5ms"},
        {"product_id": 134, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync"},
        {"product_id": 134, "parameter_name": "Color Gamut", "specification": "IPS Wide Viewing Angles"},
        {"product_id": 134, "parameter_name": "Connectivity", "specification": "HDMI, VGA"},
        {"product_id": 134, "parameter_name": "Stand Adjustments", "specification": "Tilt"},
        {"product_id": 134, "parameter_name": "Ergonomic Features", "specification": "Adjustable Tilt, Eye Comfort Technologies"},

        {"product_id": 135, "parameter_name": "Display Size", "specification": "24-inch"},
        {"product_id": 135, "parameter_name": "Resolution", "specification": "1920x1080 (Full HD)"},
        {"product_id": 135, "parameter_name": "Panel Type", "specification": "TN"},
        {"product_id": 135, "parameter_name": "Refresh Rate", "specification": "240Hz"},
        {"product_id": 135, "parameter_name": "Response Time", "specification": "0.5ms (GtG)"},
        {"product_id": 135, "parameter_name": "Adaptive Sync", "specification": "AMD FreeSync Premium"},
        {"product_id": 135, "parameter_name": "Color Gamut", "specification": "99% sRGB"},
        {"product_id": 135, "parameter_name": "Connectivity", "specification": "HDMI, DisplayPort"},
        {"product_id": 135, "parameter_name": "Stand Adjustments", "specification": "Tilt, Swivel, Height"},
        {"product_id": 135, "parameter_name": "Ergonomic and Design Features", "specification": "Adjustable Stand, RGB Lighting"},

        {"product_id": 136, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 6E (a/b/g/n/ac/ax/be)"},
        {"product_id": 136, "parameter_name": "Maximum Speed", "specification": "12000Mb/s"},
        {"product_id": 136, "parameter_name": "Bands", "specification": "Tri-Band"},
        {"product_id": 136, "parameter_name": "Beamforming", "specification": "Yes"},
        {"product_id": 136, "parameter_name": "Security", "specification": "Netgear Armor"},
        {"product_id": 136, "parameter_name": "Ethernet Ports", "specification": "Multi-Gigabit Ethernet"},
        {"product_id": 136, "parameter_name": "USB Ports", "specification": "None"},
        {"product_id": 136, "parameter_name": "Antenna Type", "specification": "External"},
        {"product_id": 136, "parameter_name": "Dimensions", "specification": "Approx. 12.5 x 8 x 4.5 inches"},
        {"product_id": 136, "parameter_name": "Weight", "specification": "2.5 lbs"},

        {"product_id": 137, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 6 (a/b/g/n/ac/ax)"},
        {"product_id": 137, "parameter_name": "Maximum Speed", "specification": "3000Mb/s"},
        {"product_id": 137, "parameter_name": "Bands", "specification": "Dual-Band"},
        {"product_id": 137, "parameter_name": "Beamforming", "specification": "Yes"},
        {"product_id": 137, "parameter_name": "Security", "specification": "WPA3"},
        {"product_id": 137, "parameter_name": "Ethernet Ports", "specification": "Gigabit LAN"},
        {"product_id": 137, "parameter_name": "USB Ports", "specification": "USB 3.0"},
        {"product_id": 137, "parameter_name": "Antenna Type", "specification": "Internal"},
        {"product_id": 137, "parameter_name": "Dimensions", "specification": "Approx. 11.2 x 8.5 x 3.4 inches"},
        {"product_id": 137, "parameter_name": "Weight", "specification": "1.5 lbs"},

        {"product_id": 138, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 6 (a/b/g/n/ac/ax)"},
        {"product_id": 138, "parameter_name": "Maximum Speed", "specification": "1800Mb/s"},
        {"product_id": 138, "parameter_name": "Bands", "specification": "Dual-Band"},
        {"product_id": 138, "parameter_name": "Beamforming", "specification": "Yes"},
        {"product_id": 138, "parameter_name": "Security", "specification": "WPA3"},
        {"product_id": 138, "parameter_name": "Ethernet Ports", "specification": "Gigabit LAN"},
        {"product_id": 138, "parameter_name": "USB Ports", "specification": "None"},
        {"product_id": 138, "parameter_name": "Antenna Type", "specification": "Internal"},
        {"product_id": 138, "parameter_name": "Dimensions", "specification": "Approx. 10.5 x 7.8 x 2.9 inches"},
        {"product_id": 138, "parameter_name": "Weight", "specification": "1.3 lbs"},

        {"product_id": 139, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 6E (a/b/g/n/ac/ax/be)"},
        {"product_id": 139, "parameter_name": "Maximum Speed", "specification": "3600Mb/s"},
        {"product_id": 139, "parameter_name": "Bands", "specification": "Tri-Band"},
        {"product_id": 139, "parameter_name": "Beamforming", "specification": "Yes"},
        {"product_id": 139, "parameter_name": "Security", "specification": "TP-Link HomeCare™"},
        {"product_id": 139, "parameter_name": "Ethernet Ports", "specification": "Multi-Gigabit LAN"},
        {"product_id": 139, "parameter_name": "USB Ports", "specification": "USB 3.0"},
        {"product_id": 139, "parameter_name": "Antenna Type", "specification": "External"},
        {"product_id": 139, "parameter_name": "Dimensions", "specification": "Approx. 13.0 x 9.0 x 5.0 inches"},
        {"product_id": 139, "parameter_name": "Weight", "specification": "3.0 lbs"},

        {"product_id": 140, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 5 (a/b/g/n/ac)"},
        {"product_id": 140, "parameter_name": "Maximum Speed", "specification": "1200Mb/s"},
        {"product_id": 140, "parameter_name": "Bands", "specification": "Dual-Band"},
        {"product_id": 140, "parameter_name": "Beamforming", "specification": "Yes"},
        {"product_id": 140, "parameter_name": "Security", "specification": "WPA3"},
        {"product_id": 140, "parameter_name": "Ethernet Ports", "specification": "Gigabit LAN"},
        {"product_id": 140, "parameter_name": "USB Ports", "specification": "None"},
        {"product_id": 140, "parameter_name": "Antenna Type", "specification": "Internal"},
        {"product_id": 140, "parameter_name": "Dimensions", "specification": "Approx. 10.2 x 7.4 x 3.0 inches"},
        {"product_id": 140, "parameter_name": "Weight", "specification": "1.1 lbs"},

        {"product_id": 141, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 6 (a/b/g/n/ac/ax)"},
        {"product_id": 141, "parameter_name": "Maximum Speed", "specification": "1800Mb/s"},
        {"product_id": 141, "parameter_name": "Bands", "specification": "Dual-Band"},
        {"product_id": 141, "parameter_name": "Beamforming", "specification": "Yes"},
        {"product_id": 141, "parameter_name": "Security", "specification": "AiProtection"},
        {"product_id": 141, "parameter_name": "Ethernet Ports", "specification": "3x Gigabit LAN"},
        {"product_id": 141, "parameter_name": "USB Ports", "specification": "1x USB 3.0"},
        {"product_id": 141, "parameter_name": "Antenna Type", "specification": "Internal"},
        {"product_id": 141, "parameter_name": "Dimensions", "specification": "Approx. 11.0 x 8.0 x 3.5 inches"},
        {"product_id": 141, "parameter_name": "Weight", "specification": "1.8 lbs"},

        {"product_id": 142, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 5 (a/b/g/n/ac)"},
        {"product_id": 142, "parameter_name": "Maximum Speed", "specification": "750Mbps"},
        {"product_id": 142, "parameter_name": "Bands", "specification": "Dual-Band"},
        {"product_id": 142, "parameter_name": "Beamforming", "specification": "Yes"},
        {"product_id": 142, "parameter_name": "Security", "specification": "WPA3"},
        {"product_id": 142, "parameter_name": "Ethernet Ports", "specification": "4x Gigabit LAN"},
        {"product_id": 142, "parameter_name": "USB Ports", "specification": "None"},
        {"product_id": 142, "parameter_name": "Antenna Type", "specification": "External"},
        {"product_id": 142, "parameter_name": "Dimensions", "specification": "Approx. 12.0 x 8.5 x 4.0 inches"},
        {"product_id": 142, "parameter_name": "Weight", "specification": "2.2 lbs"},

        {"product_id": 143, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 6 (a/b/g/n/ac/ax)"},
        {"product_id": 143, "parameter_name": "Maximum Speed", "specification": "3000Mb/s"},
        {"product_id": 143, "parameter_name": "Bands", "specification": "Tri-Band"},
        {"product_id": 143, "parameter_name": "Beamforming+", "specification": "Yes"},
        {"product_id": 143, "parameter_name": "Security", "specification": "WPA3"},
        {"product_id": 143, "parameter_name": "Ethernet Ports", "specification": "4x Gigabit LAN"},
        {"product_id": 143, "parameter_name": "USB Ports", "specification": "None"},
        {"product_id": 143, "parameter_name": "Antenna Type", "specification": "Internal"},
        {"product_id": 143, "parameter_name": "Dimensions", "specification": "Approx. 12.0 x 8.0 x 3.5 inches"},
        {"product_id": 143, "parameter_name": "Weight", "specification": "2.0 lbs"},

        {"product_id": 144, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 6 (a/b/g/n/ac/ax)"},
        {"product_id": 144, "parameter_name": "Maximum Speed", "specification": "4670Mb/s"},
        {"product_id": 144, "parameter_name": "Bands", "specification": "Tri-Band"},
        {"product_id": 144, "parameter_name": "Beamforming+", "specification": "Yes"},
        {"product_id": 144, "parameter_name": "Security", "specification": "WPA3"},
        {"product_id": 144, "parameter_name": "Ethernet Ports", "specification": "2x Multi-Gigabit LAN"},
        {"product_id": 144, "parameter_name": "USB Ports", "specification": "None"},
        {"product_id": 144, "parameter_name": "Antenna Type", "specification": "External"},
        {"product_id": 144, "parameter_name": "Dimensions", "specification": "Approx. 14.0 x 10.0 x 5.0 inches"},
        {"product_id": 144, "parameter_name": "Weight", "specification": "3.5 lbs"},

        {"product_id": 145, "parameter_name": "Wi-Fi Standard", "specification": "Wi-Fi 6 (a/b/g/n/ac/ax)"},
        {"product_id": 145, "parameter_name": "Maximum Speed", "specification": "3000Mb/s"},
        {"product_id": 145, "parameter_name": "Bands", "specification": "Dual-Band"},
        {"product_id": 145, "parameter_name": "Beamforming+", "specification": "Yes"},
        {"product_id": 145, "parameter_name": "Security", "specification": "AiProtection"},
        {"product_id": 145, "parameter_name": "Ethernet Ports", "specification": "4x Gigabit LAN"},
        {"product_id": 145, "parameter_name": "USB Ports", "specification": "1x USB 3.0"},
        {"product_id": 145, "parameter_name": "Antenna Type", "specification": "Internal"},
        {"product_id": 145, "parameter_name": "Dimensions", "specification": "Approx. 12.5 x 8.5 x 4.0 inches"},
        {"product_id": 145, "parameter_name": "Weight", "specification": "2.8 lbs"},

        {"product_id": 146, "parameter_name": "Cable Type", "specification": "USB-C to USB-C"},
        {"product_id": 146, "parameter_name": "Power Delivery", "specification": "100W"},
        {"product_id": 146, "parameter_name": "Length", "specification": "2 meters"},
        {"product_id": 146, "parameter_name": "Data Transfer Speed", "specification": "10Gbps"},
        {"product_id": 146, "parameter_name": "Material", "specification": "Braided Nylon"},
        {"product_id": 146, "parameter_name": "Compatibility", "specification": "USB-C devices (smartphones, tablets, laptops)"},
        {"product_id": 146, "parameter_name": "Connector Type", "specification": "USB-C"},
        {"product_id": 146, "parameter_name": "Shielding", "specification": "High-quality shielding to prevent interference"},
        {"product_id": 146, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 146, "parameter_name": "Additional Features", "specification": "Reinforced connectors for durability"},

        {"product_id": 147, "parameter_name": "Cable Type", "specification": "HDMI 2.1"},
        {"product_id": 147, "parameter_name": "Maximum Resolution", "specification": "8K@60Hz"},
        {"product_id": 147, "parameter_name": "Bandwidth", "specification": "48Gbps"},
        {"product_id": 147, "parameter_name": "Length", "specification": "3 meters"},
        {"product_id": 147, "parameter_name": "Material", "specification": "Braided Nylon"},
        {"product_id": 147, "parameter_name": "Connector Type", "specification": "HDMI"},
        {"product_id": 147, "parameter_name": "Shielding", "specification": "Enhanced shielding to reduce signal loss"},
        {"product_id": 147, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 147, "parameter_name": "Additional Features", "specification": "Gold-plated connectors for improved signal quality"},
        {"product_id": 147, "parameter_name": "Flexibility", "specification": "Flexible and easy to install"},

        {"product_id": 148, "parameter_name": "Cable Type", "specification": "USB-C to USB-C"},
        {"product_id": 148, "parameter_name": "Power Delivery", "specification": "100W"},
        {"product_id": 148, "parameter_name": "Length", "specification": "1 meter"},
        {"product_id": 148, "parameter_name": "Data Transfer Speed", "specification": "5Gbps"},
        {"product_id": 148, "parameter_name": "Material", "specification": "Durable PVC"},
        {"product_id": 148, "parameter_name": "Compatibility", "specification": "USB-C 3.0 devices"},
        {"product_id": 148, "parameter_name": "Connector Type", "specification": "USB-C"},
        {"product_id": 148, "parameter_name": "Shielding", "specification": "Braided exterior for durability"},
        {"product_id": 148, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 148, "parameter_name": "Additional Features", "specification": "Fast charging and data transfer"},

        {"product_id": 149, "parameter_name": "Cable Type", "specification": "DisplayPort 1.4"},
        {"product_id": 149, "parameter_name": "Maximum Resolution", "specification": "8K@60Hz"},
        {"product_id": 149, "parameter_name": "Bandwidth", "specification": "32.4Gbps"},
        {"product_id": 149, "parameter_name": "Length", "specification": "3 meters"},
        {"product_id": 149, "parameter_name": "Material", "specification": "Braided Nylon"},
        {"product_id": 149, "parameter_name": "Connector Type", "specification": "DisplayPort"},
        {"product_id": 149, "parameter_name": "Shielding", "specification": "Advanced shielding to prevent interference"},
        {"product_id": 149, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 149, "parameter_name": "Additional Features", "specification": "Flexible and easy to install"},
        {"product_id": 149, "parameter_name": "Compatibility", "specification": "DisplayPort 1.4 devices"},

        {"product_id": 150, "parameter_name": "Cable Type", "specification": "DisplayPort to HDMI"},
        {"product_id": 150, "parameter_name": "Maximum Resolution", "specification": "4K@60Hz"},
        {"product_id": 150, "parameter_name": "Length", "specification": "1.8 meters"},
        {"product_id": 150, "parameter_name": "Material", "specification": "Braided Nylon"},
        {"product_id": 150, "parameter_name": "Connector Type", "specification": "DisplayPort to HDMI"},
        {"product_id": 150, "parameter_name": "Shielding", "specification": "Enhanced shielding to reduce signal loss"},
        {"product_id": 150, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 150, "parameter_name": "Additional Features", "specification": "Plug-and-play functionality"},
        {"product_id": 150, "parameter_name": "Compatibility", "specification": "DisplayPort and HDMI devices"},
        {"product_id": 150, "parameter_name": "Flexibility", "specification": "Slim and flexible design"},

        {"product_id": 151, "parameter_name": "Cable Type", "specification": "USB-A to USB-C"},
        {"product_id": 151, "parameter_name": "Power Delivery", "specification": "45W"},
        {"product_id": 151, "parameter_name": "Length", "specification": "1 meter"},
        {"product_id": 151, "parameter_name": "Data Transfer Speed", "specification": "5Gbps"},
        {"product_id": 151, "parameter_name": "Material", "specification": "Braided Nylon"},
        {"product_id": 151, "parameter_name": "Compatibility", "specification": "USB-A and USB-C devices"},
        {"product_id": 151, "parameter_name": "Connector Type", "specification": "USB-A and USB-C"},
        {"product_id": 151, "parameter_name": "Shielding", "specification": "Braided exterior to prevent tangling"},
        {"product_id": 151, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 151, "parameter_name": "Additional Features", "specification": "Reinforced connectors for durability"},

        {"product_id": 152, "parameter_name": "Adapter Type", "specification": "USB-C to Minijack"},
        {"product_id": 152, "parameter_name": "Power Output", "specification": "3.5W"},
        {"product_id": 152, "parameter_name": "Compatibility", "specification": "USB-C devices with minijack headphones"},
        {"product_id": 152, "parameter_name": "Connector Type", "specification": "USB-C and 3.5mm minijack"},
        {"product_id": 152, "parameter_name": "Material", "specification": "Durable plastic"},
        {"product_id": 152, "parameter_name": "Size", "specification": "Compact and portable"},
        {"product_id": 152, "parameter_name": "Shielding", "specification": "Minimal interference"},
        {"product_id": 152, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 152, "parameter_name": "Additional Features", "specification": "Plug-and-play functionality"},
        {"product_id": 152, "parameter_name": "Flexibility", "specification": "Slim design for easy use"},

        {"product_id": 153, "parameter_name": "Cable Type", "specification": "RJ-45 to RJ-45 UTP Cat.6"},
        {"product_id": 153, "parameter_name": "Length", "specification": "2 meters"},
        {"product_id": 153, "parameter_name": "Data Transfer Speed", "specification": "1Gbps"},
        {"product_id": 153, "parameter_name": "Material", "specification": "Twisted Pair Copper"},
        {"product_id": 153, "parameter_name": "Connector Type", "specification": "RJ-45"},
        {"product_id": 153, "parameter_name": "Shielding", "specification": "Shielded Twisted Pair"},
        {"product_id": 153, "parameter_name": "Color", "specification": "Blue"},
        {"product_id": 153, "parameter_name": "Additional Features", "specification": "Flat design for easy cable management"},
        {"product_id": 153, "parameter_name": "Compatibility", "specification": "Networking devices (routers, switches, PCs)"},
        {"product_id": 153, "parameter_name": "Durability", "specification": "High durability for long-term use"},

        {"product_id": 154, "parameter_name": "Cable Type", "specification": "SATA III"},
        {"product_id": 154, "parameter_name": "Length", "specification": "0.5 meters"},
        {"product_id": 154, "parameter_name": "Connector Type", "specification": "SATA III"},
        {"product_id": 154, "parameter_name": "Design", "specification": "Angled connector"},
        {"product_id": 154, "parameter_name": "Material", "specification": "Flexible PVC"},
        {"product_id": 154, "parameter_name": "Data Transfer Speed", "specification": "6Gbps"},
        {"product_id": 154, "parameter_name": "Compatibility", "specification": "SATA III devices (SSDs, HDDs)"},
        {"product_id": 154, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 154, "parameter_name": "Additional Features", "specification": "Reinforced connectors for durability"},
        {"product_id": 154, "parameter_name": "Flexibility", "specification": "Flexible design for easy installation"},

        {"product_id": 155, "parameter_name": "Cable Type", "specification": "SCHUKO to C13 Power Cable"},
        {"product_id": 155, "parameter_name": "Length", "specification": "1.8 meters"},
        {"product_id": 155, "parameter_name": "Connector Type", "specification": "SCHUKO and C13"},
        {"product_id": 155, "parameter_name": "Material", "specification": "High-quality PVC"},
        {"product_id": 155, "parameter_name": "Power Rating", "specification": "10A"},
        {"product_id": 155, "parameter_name": "Compatibility", "specification": "Desktop computers, servers, electronic devices with C13 input"},
        {"product_id": 155, "parameter_name": "Color", "specification": "Black"},
        {"product_id": 155, "parameter_name": "Additional Features", "specification": "Reinforced plugs for durability"},
        {"product_id": 155, "parameter_name": "Safety", "specification": "Certified for safety and compliance"},
        {"product_id": 155, "parameter_name": "Design", "specification": "Tangle-free and flexible"},

    ]

    for spec in tqdm(specifications, desc="Seeding specifications", unit="spec"):
        try:
            Specification.objects.create(
                product=Product.objects.get(id=spec["product_id"]),
                parameter_name=spec["parameter_name"],
                specification=spec["specification"]
            )
            print(Fore.GREEN + f"Successfully added specification: {spec['parameter_name']} for product ID {spec['product_id']}")
        except Product.DoesNotExist:
            print(Fore.RED + f"Product with ID {spec['product_id']} does not exist. Skipping specification: {spec['parameter_name']}.")
        except Exception as e:
            print(Fore.RED + f"Error adding specification {spec['parameter_name']} for product ID {spec['product_id']}: {e}")

    print(Fore.GREEN + "Specifications seeded successfully!")