"""Module to plot data"""
# third party
import pandas as pd
import matplotlib.pyplot as plt


def plot_data(df: pd.DataFrame,
              config: dict,
              save: bool=False) -> None:
    """
    Plot data of curtailed power and energy of one
    power plant.

    :param df: pandas data frame, data to plot
    :param config: dict, meta information about the data
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9, 6))
    fontsize: int = 10

    df.plot(x="start_curtailment", y="nominal_power",
            color="black", label="Power [kW]", ax=ax)
    ax.get_legend().remove()

    ax2 = ax.twinx()
    df.plot(x="start_curtailment", y="sum_energy_curtailed",
            color="yellow", label="Energy [kWh]", ax=ax2)

    ax.set_xlabel("", fontsize=fontsize)
    ax.set_ylabel("Power [kW]",fontsize=fontsize)
    ax2.set_ylabel("Energy [kWh]", fontsize=fontsize)

    handles, labels = [],[]
    for ax in fig.axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            handles.append(h)
            labels.append(l)
    plt.legend(handles, labels)

    plt.title(f"Plant ID: {config['plant_id']}, Selected Levels: {config['level']}",
              fontsize=fontsize)
    plt.tight_layout()
    if save:
        plt.savefig("figure.png")
    plt.show()
