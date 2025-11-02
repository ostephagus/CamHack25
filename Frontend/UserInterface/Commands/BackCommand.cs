using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using UserInterface.ViewModels;
using UserInterface.Views;

namespace UserInterface.Commands
{
    public class BackCommand : ICommand
    {
        public event EventHandler? CanExecuteChanged;

        private App parentApp;

        public bool CanExecute(object? parameter)
        {
            return true;
        }

        public void Execute(object? parameter)
        {
            parentApp.SwitchWindow(new SearchScreen(), new SearchScreenVM(new Commands.SearchCommand(parentApp)));
        }

        public BackCommand(App parentApp)
        {
            this.parentApp = parentApp;
        }
    }
}
