using System;
using System.Collections.Generic;
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
            // Run python script here.
            MessageBox.Show("Python script not yet attached.");
        }
    }
}
