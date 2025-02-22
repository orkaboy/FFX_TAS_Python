import memory.main
import pathing
import xbox
from paths import MiihenAgency
from players import Kimahri, Tidus, Wakka

FFXC = xbox.controller_handle()


def engage():
    checkpoint = 0
    input("Confirm that CSR is running!!!")
    while not memory.main.battle_active():
        if memory.main.user_control():
            memory.main.get_item_slot(6)
            if memory.main.get_map() == 58:
                memory.main.update_formation(Tidus, Kimahri, Wakka)
                FFXC.set_movement(0, 1)
                memory.main.await_event()
                FFXC.set_neutral()
            # elif checkpoint == 2 and memory.main.get_item_count_slot(p_down_slot) >= 10:
            #    checkpoint = 4
            elif checkpoint in [2, 3]:
                checkpoint = 4
            elif checkpoint == 5:
                FFXC.set_movement(0, -1)
                memory.main.await_event()
                FFXC.set_neutral()
                checkpoint = 4
            elif pathing.set_movement(MiihenAgency.execute(checkpoint)):
                checkpoint += 1
                print("Checkpoint", checkpoint)
        else:
            FFXC.set_neutral()
            if memory.main.diag_skip_possible():
                xbox.tap_b()


def battle():
    memory.main.wait_frames(10)
    choco_index = memory.main.actor_index(actor_num=4200)
    # "choco_coords" is assigned to but not used
    # choco_coords = memory.main.get_actor_coords(actor_number=choco_index)
    input("Ready 1")
    memory.main.choco_eater_fun(actor_index=choco_index)
    input("Ready 2")
    xbox.tap_up()
    xbox.tap_up()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    xbox.tap_b()
    exit()
