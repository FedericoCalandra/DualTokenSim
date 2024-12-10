import tkinter
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
import os


class GUIParamInitializer:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "../build/assets/frame0")
        self.ASSETS_PATH = (Path(filename))
        self.simulation_parameters = None
        self.display_gui()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def display_gui(self):
        window = Tk()

        window.geometry("1024x640")
        window.configure(bg="#EBEBEB")

        canvas = Canvas(
            window,
            bg="#EBEBEB",
            height=640,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_text(
            384.0,
            40.0,
            anchor="nw",
            text="Set Simulation Parameters",
            fill="#000000",
            font=("Inter SemiBold", 20 * -1)
        )

        canvas.create_text(
            339.0,
            110.0,
            anchor="nw",
            text="Stablecoin",
            fill="#000000",
            font=("Inter", 14 * -1)
        )

        canvas.create_text(
            447.0,
            341.0,
            anchor="nw",
            text="Virtual Liquidity Pool",
            fill="#000000",
            font=("Inter", 14 * -1)
        )

        entry_image_1 = PhotoImage(
            file=self.relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            374.0,
            164.5,
            image=entry_image_1
        )
        entry_st_price = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_st_price.place(
            x=310.0,
            y=152.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            272.0,
            158.0,
            anchor="nw",
            text="Price",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        canvas.create_text(
            321.0,
            397.0,
            anchor="nw",
            text="Algorithm",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        canvas.create_text(
            243.0,
            438.0,
            anchor="nw",
            text="Stablecoin base quantity",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        canvas.create_text(
            264.0,
            479.0,
            anchor="nw",
            text="Pool recovery period",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        entry_image_2 = PhotoImage(
            file=self.relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            374.0,
            246.5,
            image=entry_image_2
        )
        entry_st_free = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_st_free.place(
            x=310.0,
            y=234.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            238.0,
            240.0,
            anchor="nw",
            text="Free supply",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        entry_image_3 = PhotoImage(
            file=self.relative_to_assets("entry_3.png"))
        entry_bg_3 = canvas.create_image(
            374.0,
            287.5,
            image=entry_image_3
        )
        entry_st_fee = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_st_fee.place(
            x=310.0,
            y=275.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            256.0,
            281.0,
            anchor="nw",
            text="Pool fee",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        entry_image_4 = PhotoImage(
            file=self.relative_to_assets("entry_4.png"))
        entry_bg_4 = canvas.create_image(
            725.0,
            287.5,
            image=entry_image_4
        )
        entry_ct_fee = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_ct_fee.place(
            x=661.0,
            y=275.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            607.0,
            281.0,
            anchor="nw",
            text="Pool fee",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        entry_image_5 = PhotoImage(
            file=self.relative_to_assets("entry_5.png"))
        entry_bg_5 = canvas.create_image(
            374.0,
            205.5,
            image=entry_image_5
        )
        entry_st_supply = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_st_supply.place(
            x=310.0,
            y=193.0,
            width=128.0,
            height=23.0
        )

        entry_image_6 = PhotoImage(
            file=self.relative_to_assets("entry_6.png"))
        entry_bg_6 = canvas.create_image(
            515.0,
            485.5,
            image=entry_image_6
        )
        entry_vlp_pool_recovery = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_vlp_pool_recovery.place(
            x=451.0,
            y=473.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            329.0,
            520.0,
            anchor="nw",
            text="Pool fee",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        entry_image_7 = PhotoImage(
            file=self.relative_to_assets("entry_7.png"))
        entry_bg_7 = canvas.create_image(
            515.0,
            526.5,
            image=entry_image_7
        )
        entry_vlp_fee = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_vlp_fee.place(
            x=451.0,
            y=514.0,
            width=128.0,
            height=23.0
        )

        entry_image_8 = PhotoImage(
            file=self.relative_to_assets("entry_8.png"))
        entry_bg_8 = canvas.create_image(
            515.0,
            444.5,
            image=entry_image_8
        )
        entry_vlp_base = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_vlp_base.place(
            x=451.0,
            y=432.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            263.0,
            199.0,
            anchor="nw",
            text="Supply",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        canvas.create_text(
            693.0,
            110.0,
            anchor="nw",
            text="Collateral",
            fill="#000000",
            font=("Inter", 14 * -1)
        )

        entry_image_9 = PhotoImage(
            file=self.relative_to_assets("entry_9.png"))
        entry_bg_9 = canvas.create_image(
            725.0,
            164.5,
            image=entry_image_9
        )
        entry_ct_price = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_ct_price.place(
            x=661.0,
            y=152.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            623.0,
            158.0,
            anchor="nw",
            text="Price",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        entry_image_10 = PhotoImage(
            file=self.relative_to_assets("entry_10.png"))
        entry_bg_10 = canvas.create_image(
            725.0,
            246.5,
            image=entry_image_10
        )
        entry_ct_free = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_ct_free.place(
            x=661.0,
            y=234.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            589.0,
            240.0,
            anchor="nw",
            text="Free supply",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        entry_image_11 = PhotoImage(
            file=self.relative_to_assets("entry_11.png"))
        entry_bg_11 = canvas.create_image(
            725.0,
            205.5,
            image=entry_image_11
        )
        entry_ct_supply = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_ct_supply.place(
            x=661.0,
            y=193.0,
            width=128.0,
            height=23.0
        )

        canvas.create_text(
            614.0,
            199.0,
            anchor="nw",
            text="Supply",
            fill="#000000",
            font=("Inter", 11 * -1)
        )

        def start_simulation():
            st_price = entry_st_price.get()
            st_supply = entry_st_supply.get()
            st_free = entry_st_free.get()
            st_pool_fee = entry_st_fee.get()
            ct_price = entry_ct_price.get()
            ct_supply = entry_ct_supply.get()
            ct_free = entry_ct_free.get()
            ct_pool_fee = entry_ct_fee.get()
            vlp_base = entry_vlp_base.get()
            vlp_pool_recovery = entry_vlp_pool_recovery.get()
            vlp_pool_fee = entry_vlp_fee.get()

            self.simulation_parameters = {
                "stablecoin": {
                    "price": st_price,
                    "supply": st_supply,
                    "free_supply": st_free,
                    "pool_fee": st_pool_fee,
                },
                "collateral_token": {
                    "price": ct_price,
                    "supply": ct_supply,
                    "free_supply": ct_free,
                    "pool_fee": ct_pool_fee,
                },
                "virtual_liquidity_pool": {
                    "base": vlp_base,
                    "pool_recovery": vlp_pool_recovery,
                    "pool_fee": vlp_pool_fee,
                }
            }

            window.destroy()

        button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=426.0,
            y=391.0,
            width=86.0,
            height=25.0
        )

        button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=start_simulation,
            relief="flat"
        )
        button_2.place(
            x=448.0,
            y=570.0,
            width=132.0,
            height=25.0
        )

        button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
        button_3 = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        button_3.place(
            x=518.0,
            y=391.0,
            width=86.0,
            height=25.0
        )

        entry_st_price.insert(tkinter.END, "1.0")
        entry_st_supply.insert(tkinter.END, "10000")
        entry_st_free.insert(tkinter.END, "5000")
        entry_st_fee.insert(tkinter.END, "0.01")

        entry_ct_price.insert(tkinter.END, "5.0")
        entry_ct_supply.insert(tkinter.END, "10000")
        entry_ct_free.insert(tkinter.END, "5000")
        entry_ct_fee.insert(tkinter.END, "0.01")

        entry_vlp_base.insert(tkinter.END, "1000")
        entry_vlp_pool_recovery.insert(tkinter.END, "10")
        entry_vlp_fee.insert(tkinter.END, "0.01")

        window.resizable(False, False)
        window.mainloop()

