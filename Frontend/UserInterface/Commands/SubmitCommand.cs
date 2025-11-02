using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using UserInterface.ViewModels;

namespace UserInterface.Commands
{
    public class SubmitCommand : ICommand
    {
        SearchResultsScreenVM parentViewModel;

        public SubmitCommand(SearchResultsScreenVM parentViewModel)
        {
            this.parentViewModel = parentViewModel;
        }

        public event EventHandler? CanExecuteChanged;

        public bool CanExecute(object? parameter)
        {
            return parentViewModel.SelectedMolecule != "";
        }

        public void OnCanExecuteChanged(object sender, EventArgs e)
        {
            CanExecuteChanged?.Invoke(sender, e);
        }

        public void Execute(object? parameter)
        {
            string selectedMolecule = parentViewModel.SelectedMolecule;
            try
            {
                ProcessStartInfo startInfo = new ProcessStartInfo
                {
                    FileName = "cmd.exe",
                    Arguments = $"/c python {ProjectInfo.BuildInfo.SolutionDir}/../wrapper.py {selectedMolecule}",
                    UseShellExecute = true,
                    CreateNoWindow = false,
                    WorkingDirectory = $"{ProjectInfo.BuildInfo.SolutionDir}/.."
                };
                Process.Start(startInfo);
                MessageBox.Show("Process started.");

            }
            catch (Exception e)
            {
                MessageBox.Show($"Execution of python script failed: {e.Message}");
            }
        }
    }
}
