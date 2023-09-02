from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# Constants
SOLAR_PANEL_EFFICIENCY = 0.15
COST_PER_UNIT_CURRENT_INR = 75000
WATT_PER_SQUARE_METER = 150
GRID_EMISSIONS_FACTOR = 0.6  # CO2 emissions factor for grid electricity (example value)
CO2_ABSORBED_PER_TREE_PER_YEAR = 22.6  # Example value, CO2 absorbed by one tree per year in kg

# Initialize area_required_sqft as None
area_required_sqft = None

class SolarEnergyCalculatorApp(App):

    def build(self):
        self.title = "Solar Energy Calculator"
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.units_label = Label(text="Enter your average monthly electricity consumption (units of current):")
        self.layout.add_widget(self.units_label)

        self.units_entry = TextInput(multiline=False)
        self.layout.add_widget(self.units_entry)

        self.calculate_button = Button(text="Calculate")
        self.calculate_button.bind(on_press=self.calculate_solar_energy)
        self.layout.add_widget(self.calculate_button)

        self.result_label = Label(text="")
        self.layout.add_widget(self.result_label)

        self.sunlight_hours_label = Label(text="Number of sunlight hours per day:")
        self.layout.add_widget(self.sunlight_hours_label)

        self.sunlight_hours_entry = TextInput(multiline=False, readonly=True)
        self.layout.add_widget(self.sunlight_hours_entry)

        self.calculate_sunlight_button = Button(text="Calculate Solar Energy Production")
        self.calculate_sunlight_button.bind(on_press=self.calculate_solar_energy_with_sunlight_hours)
        self.layout.add_widget(self.calculate_sunlight_button)

        self.result_label_2 = Label(text="")
        self.layout.add_widget(self.result_label_2)

        return self.layout

    def calculate_solar_energy(self, instance):
        global area_required_sqft

        current_units = float(self.units_entry.text)

        area_required_sqft = current_units

        total_cost_inr = current_units * COST_PER_UNIT_CURRENT_INR / 1000

        battery_storage_kWh = current_units

        solar_panels_watts = current_units * 10 / 1000

        electric_bill = 0
        if current_units < 200:
            electric_bill = current_units * 1.49
        else:
            electric_bill = current_units * 2

        bill_reduction = electric_bill * 90 / 100

        self.result_label.text = (f"Estimated Area Required: {area_required_sqft:.2f} square feet\n"
                                   f"Total Cost of Solar Panels: ₹{total_cost_inr:.2f}\n"
                                   f"Battery Storage Required: {battery_storage_kWh:.2f} kWh\n"
                                   f"Solar Panels Required: {solar_panels_watts:.2f} kW\n"
                                   f"Estimated Monthly Electric Bill reduction: ₹{bill_reduction:.2f}\n"
                                   f"Please enter the number of sunlight hours per day:")

        self.sunlight_hours_entry.readonly = False

    def calculate_solar_energy_with_sunlight_hours(self, instance):
        global area_required_sqft

        sunlight_hours_per_day = float(self.sunlight_hours_entry.text)

        solar_energy_production = area_required_sqft * sunlight_hours_per_day * SOLAR_PANEL_EFFICIENCY

        co2_reduction = solar_energy_production * GRID_EMISSIONS_FACTOR

        trees_saved = co2_reduction / CO2_ABSORBED_PER_TREE_PER_YEAR

        new_output = (f"\nSunlight Hours per Day: {sunlight_hours_per_day:.2f}\n"
                      f"Solar Energy Production: {solar_energy_production:.2f} kWh per day\n"
                      f"Estimated CO2 Emissions Reduction: {co2_reduction:.2f} kg CO2 per day\n"
                      f"Estimated Number of Trees Saved: {trees_saved:.2f} trees per day")
        self.result_label_2.text = new_output

if __name__ == '__main__':
    SolarEnergyCalculatorApp().run()

