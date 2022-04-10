import plotly.express as px


class VisualizeRaw:
    def __init__(self, df, time_col) -> None:
        self.df = df
        self.time = time_col
        self.trial_data = []
        
    def start_indices(self):
        """Finds all indices where time resets to 0 seconds (start of trial).

        :return: Time zero indices
        :rtype: list[int]
        """
        return list(self.df[self.df[self.time] == 0].index)
    
    def split_trials(self):
        """Breaks dataframe into individual trials."""
        
        start_indices = self.start_indices()
        
        for i, start_inx in enumerate(start_indices):
            end_inx = start_indices[i + 1] if i != len(start_indices) - 1 else len(self.df)
            self.trial_data.append(self.df.iloc[start_inx:end_inx])
        
        # Ensure that all the data is accounted for
        assert len(start_indices) == len(self.trial_data)
    
    def plot_trials(self, dir_path, column):
        """Plots each trial seperately for manual visualization. Saves plots in directory.

        :param dir_path: Output directory for plots
        :type dir_path: str
        :param column: Name of column in DataFrame to plot
        :type column: str
        """
        for i, trial in enumerate(self.trial_data):
            fig = px.line(x=trial[self.time], y=trial[column])
            fig.write_html('{0}/{1}_trial{2}.html'.format(dir_path, column, i))
            
    def plot_columns(self, dir_path, ex_num):
        """Plots each column in DataFrame separately. Saves plots in directory.

        :param dir_path: Output directory for plots
        :type dir_path: str
        :param ex_num: Exercise number used for name scheme
        :type ex_num: int
        """
        columns = list(self.df.columns)
        columns.pop(columns.index(self.time))
        figs = [px.line(x=self.df[self.time], y=self.df[col]) for col in columns]
        [x.write_html('{0}/{1}{2}.html'.format(dir_path, col, ex_num)) for x, col in zip(figs, columns)]
            
    def pull_trial_df(self, trial_num, filename, ext='xlsx'):
        """Exports DataFrame of a single trial.

        :param trial_num: Number of trial to export
        :type trial_num: int
        :param filename: Name of file to save DataFrame to
        :type filename: str
        :param ext: File extension to save to, defaults to 'xlsx'
        :type ext: str, optional
        :raises ValueError: Unrecognized file extension.
        """
        if ext == 'xlsx':
            self.trial_data[trial_num].to_excel(f'{filename}.xlsx', index=False)
        elif ext == 'csv':
            self.trial_data[trial_num].to_csv(f'{filename}.csv', index=False)
        else:
            raise ValueError(f'{ext} is not a recognized file extension.')
