import seaborn as sns
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df
from shiny import App, reactive, render, ui

Countries = df["Country Name"]
Countries = Countries.to_list()
years = [ '2015', '2019', '2020', '2021', '2022']  

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_switch("switch", "Select all", True),
        ui.input_checkbox_group(
            "countries",
            "Countries",
            Countries,
            selected=Countries,
        ),
        title="Filter controls",
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Summary statistics"),
            ui.output_data_frame("summary_statistics"),
            full_screen=True,
        ),
    ),
    ui.include_css(app_dir / "styles.css"),
    title="Inflation dashboard",
    fillable=True,
)


def server(input, output, session):
    @reactive.calc
    def filtered_df():
        filt_df = df[df["Country Name"].isin(input.countries())]
        return filt_df

    @reactive.effect
    def _():
        choices = Countries if input.switch() else []
        ui.update_checkbox_group("countries",selected=choices)
        swicth_name = "Select all" if input.switch() else "Deselect all"
        ui.update_switch("switch",label=swicth_name)


    @render.data_frame
    def summary_statistics():
        cols = [
            "Country Name",
            *years,
        ]
        return render.DataGrid(filtered_df()[cols], filters=False)


app = App(app_ui, server)