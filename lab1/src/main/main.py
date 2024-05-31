from src.main.model.entity.enum.region import Region
from src.main.controller.cadastral_agency_controller import CadastralAgencyController
from view.menu import Menu


current_region = Region.DEFAULT
controller = CadastralAgencyController()


def save_exit():
    controller.save_all()
    exit(0)


def load():
    controller.load()


def select_region(region: Region):
    global current_region
    current_region = region


load()
print("Welcome to Cadastral Agency! Please select region.")
while current_region == Region.DEFAULT:
    current_region = controller.select_region(current_region)
while True:
    Menu.print_menu(
        ("Cadastral Agency Program - Main Menu\n"
         f"Current Region: {current_region.name}"
         ),
        {
            "Select Region": lambda: select_region(controller.select_region(current_region)),
            "Land Plot Registration": lambda: controller.land_plot_registration(current_region),
            "Building Registration": lambda: controller.building_registration(),
            "Documents & Information": lambda: controller.information_presentation(),
            (0, "Exit"): save_exit,
        },
    )

    # TEST OWNERS:
    # 1. 1234567A123BC1
    # 2. 1111111A111AA1
    # 3. 9309706H666UI0
    # 4. 0000000A000AA0
