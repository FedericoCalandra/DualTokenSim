import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from source.simulations.three_pools_live_simulation import ThreePoolsLiveSimulation


class GUIDashboard:
    def __init__(self, simulation: ThreePoolsLiveSimulation):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "../build/assets/frame0")
        self.ASSETS_PATH = (Path(filename))

        self.time_window = 100

        self.stablecoin_fig = None
        self.stablecoin_ax = None
        self.stablecoin_canvas = None
        self.collateral_fig = None
        self.collateral_ax = None
        self.collateral_canvas = None
        self.delta_fig = None
        self.delta_ax = None
        self.delta_canvas = None

        self.simulation = simulation

        self.display_gui()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def display_gui(self):
        window = Tk()

        window.geometry("1324x900")
        window.configure(bg="#EBEBEB")

        canvas = Canvas(
            window,
            bg="#EBEBEB",
            height=900,
            width=1324,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        canvas.create_rectangle(
            41.0,
            32.0,
            641.0,
            432.0,
            fill="#D9D9D9",
            outline="")

        canvas.create_rectangle(
            683.0,
            32.0,
            1283.0,
            432.0,
            fill="#D9D9D9",
            outline="")

        canvas.create_rectangle(
            41.0,
            468.0,
            641.0,
            868.0,
            fill="#D9D9D9",
            outline="")

        canvas.create_rectangle(
            695.0,
            709.0,
            936.0,
            765.0,
            fill="#D9D9D9",
            outline="")

        canvas.create_text(
            747.0,
            588.0,
            anchor="nw",
            text="Free Supply",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            850.0,
            588.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            998.0,
            660.0,
            anchor="nw",
            text="Inject custom swap",
            fill="#000000",
            font=("Inter Bold", 12 * -1)
        )

        canvas.create_text(
            933.0,
            468.0,
            anchor="nw",
            text="Simulation status",
            fill="#000000",
            font=("Inter Bold", 12 * -1)
        )

        canvas.create_text(
            690.0,
            660.0,
            anchor="nw",
            text="Simulation controller",
            fill="#000000",
            font=("Inter Bold", 12 * -1)
        )

        canvas.create_text(
            695.0,
            780.0,
            anchor="nw",
            text="Speed (blocks/s)",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        entry_image_1 = PhotoImage(
            file=self.relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            847.5,
            785.5,
            image=entry_image_1
        )
        entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=816.0,
            y=775.0,
            width=63.0,
            height=19.0
        )

        entry_image_2 = PhotoImage(
            file=self.relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            1088.5,
            761.5,
            image=entry_image_2
        )
        entry_2 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_2.place(
            x=1057.0,
            y=751.0,
            width=63.0,
            height=19.0
        )

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
            x=879.0,
            y=775.0,
            width=57.0,
            height=21.0
        )

        button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=1083.0,
            y=833.0,
            width=108.0,
            height=21.0
        )

        canvas.create_text(
            1039.0,
            694.0,
            anchor="nw",
            text="Stablecoin",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            793.0,
            500.0,
            anchor="nw",
            text="Stablecoin",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1187.0,
            694.0,
            anchor="nw",
            text="Collateral",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            961.0,
            500.0,
            anchor="nw",
            text="Collateral",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1097.0,
            500.0,
            anchor="nw",
            text="Virtual Liquidity Pool",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_rectangle(
            991.0,
            713.0,
            1283.0,
            714.0,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            991.0,
            686.0,
            992.0000051579439,
            805.0,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            991.0,
            804.0,
            1283.0,
            805.0,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            1281.9999949294788,
            688.0,
            1283.0,
            805.0,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            991.0,
            685.9999745599699,
            1283.0,
            687.0,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            1136.0,
            686.0,
            1137.0000051579439,
            805.0,
            fill="#000000",
            outline="")

        canvas.create_rectangle(
            736.0,
            519.0,
            1229.0,
            520.0,
            fill="#000000",
            outline="")

        canvas.create_text(
            1010.0,
            755.0,
            anchor="nw",
            text="Quantity",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        entry_image_3 = PhotoImage(
            file=self.relative_to_assets("entry_3.png"))
        entry_bg_3 = canvas.create_image(
            1233.5,
            761.5,
            image=entry_image_3
        )
        entry_3 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry_3.place(
            x=1202.0,
            y=751.0,
            width=63.0,
            height=19.0
        )

        canvas.create_text(
            1155.0,
            755.0,
            anchor="nw",
            text="Quantity",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            779.0,
            546.0,
            anchor="nw",
            text="Price",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            850.0,
            546.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            771.0,
            567.0,
            anchor="nw",
            text="Supply",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            850.0,
            567.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            912.0,
            588.0,
            anchor="nw",
            text="Free Supply",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1015.0,
            588.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            944.0,
            546.0,
            anchor="nw",
            text="Price",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1015.0,
            546.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            936.0,
            567.0,
            anchor="nw",
            text="Supply",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1015.0,
            567.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1107.0,
            588.0,
            anchor="nw",
            text="Delta",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1178.0,
            588.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1085.0,
            546.0,
            anchor="nw",
            text="Base Pool",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1178.0,
            546.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1112.0,
            567.0,
            anchor="nw",
            text="PRP",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
        )

        canvas.create_text(
            1178.0,
            567.0,
            anchor="nw",
            text="0.0",
            fill="#000000",
            font=("Inter Medium", 10 * -1)
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
            x=794.0,
            y=721.0,
            width=33.0,
            height=33.0
        )

        button_image_4 = PhotoImage(
            file=self.relative_to_assets("button_4.png"))
        button_4 = Button(
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        button_4.place(
            x=756.0,
            y=721.0,
            width=33.0,
            height=33.0
        )

        button_image_5 = PhotoImage(
            file=self.relative_to_assets("button_5.png"))
        button_5 = Button(
            image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        button_5.place(
            x=846.0,
            y=721.0,
            width=33.0,
            height=33.0
        )

        self.simulation.run_simulation()

        self.stablecoin_fig = Figure(figsize=(6, 4), facecolor="#D9D9D9")
        self.stablecoin_ax = self.stablecoin_fig.add_subplot()
        self.stablecoin_ax.set_facecolor("#D9D9D9")
        self.stablecoin_canvas = FigureCanvasTkAgg(figure=self.stablecoin_fig, master=window)
        self.stablecoin_canvas.get_tk_widget().place(x=45, y=32)

        self.collateral_fig = Figure(figsize=(6, 4), facecolor="#D9D9D9")
        self.collateral_ax = self.collateral_fig.add_subplot()
        self.collateral_ax.set_facecolor("#D9D9D9")
        self.collateral_canvas = FigureCanvasTkAgg(figure=self.collateral_fig, master=window)
        self.collateral_canvas.get_tk_widget().place(x=687, y=32)

        self.delta_fig = Figure(figsize=(6, 4), facecolor="#D9D9D9")
        self.delta_ax = self.delta_fig.add_subplot()
        self.delta_ax.set_facecolor("#D9D9D9")
        self.delta_canvas = FigureCanvasTkAgg(figure=self.delta_fig, master=window)
        self.delta_canvas.get_tk_widget().place(x=45, y=468)

        self.update_graphs(window)

        window.resizable(False, False)
        window.mainloop()

    def update_graphs(self, window):
        """
        Dynamically updates all graphs with the latest simulation data.
        """
        stablecoin_prices = self.simulation.stablecoin_price_history
        collateral_prices = self.simulation.collateral_price_history
        delta_variation = self.simulation.delta_variation_history

        current_iteration = self.simulation.number_of_iterations
        start_iteration = max(current_iteration - self.time_window, 0)
        x_range = range(start_iteration, current_iteration)

        stablecoin_prices_slice = stablecoin_prices[start_iteration:current_iteration]
        collateral_prices_slice = collateral_prices[start_iteration:current_iteration]

        if len(x_range) != len(stablecoin_prices_slice) or len(x_range) != len(collateral_prices_slice):
            print("Data mismatch: x_range and price slices have different lengths.")
            return

        if len(stablecoin_prices_slice) > 0 and len(collateral_prices_slice) > 0:
            # Calculate y-axis limits with buffer
            stablecoin_min = min(stablecoin_prices_slice)
            stablecoin_max = max(stablecoin_prices_slice)
            collateral_min = min(collateral_prices_slice)
            collateral_max = max(collateral_prices_slice)

            buffer_stablecoin = (stablecoin_max - stablecoin_min) + 0.1
            buffer_collateral = (collateral_max - collateral_min) + 0.1

            # Update Stablecoin Price Graph
            self.stablecoin_ax.clear()
            self.stablecoin_ax.plot(x_range, stablecoin_prices_slice)
            self.stablecoin_ax.set_title("Stablecoin Price")
            self.stablecoin_ax.set_xlabel("Time")
            self.stablecoin_ax.set_ylabel("Price")
            self.stablecoin_ax.set_xlim(start_iteration, current_iteration)
            self.stablecoin_ax.set_ylim(stablecoin_min - buffer_stablecoin, stablecoin_max + buffer_stablecoin)
            self.stablecoin_canvas.draw()

            # Update Collateral Price Graph
            self.collateral_ax.clear()
            self.collateral_ax.plot(x_range, collateral_prices_slice)
            self.collateral_ax.set_title("Collateral Price")
            self.collateral_ax.set_xlabel("Time")
            self.collateral_ax.set_ylabel("Price")
            self.collateral_ax.set_xlim(start_iteration, current_iteration)
            self.collateral_ax.set_ylim(collateral_min - buffer_collateral, collateral_max + buffer_collateral)
            self.collateral_canvas.draw()

            # Update Delta Graph
            self.delta_ax.clear()
            self.delta_ax.plot(delta_variation)
            self.delta_ax.set_title("VLP Delta")
            self.delta_ax.set_xlabel("Time")
            self.delta_ax.set_ylabel("Value")
            self.delta_ax.set_xlim(start_iteration, current_iteration)
            self.delta_canvas.draw()

            window.after(1000, lambda: self.update_graphs(window))
