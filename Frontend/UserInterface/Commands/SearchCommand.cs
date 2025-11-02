using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using Newtonsoft.Json;
using UserInterface.ViewModels;
using UserInterface.Views;

namespace UserInterface.Commands
{
    public class SearchCommand : ICommand
    {
        private App parentApp;

        public event EventHandler? CanExecuteChanged;

        public SearchCommand(App parentApp)
        {
            this.parentApp = parentApp;
        }

        public bool CanExecute(object? parameter)
        {
            return true;
        }
        private static List<string> GetSearchResults(string searchText)
        {
            RunPyScriptCommand scriptRunner = new RunPyScriptCommand($"{Paths.BaseDirectory}/../api_calls/spell_suggest.py");
            if (!scriptRunner.CanExecute(null))
            {
                MessageBox.Show("Python file not attached.");
                throw new ArgumentException("Python file not found.");
            }
            string result = scriptRunner.Execute(searchText);
            List<string>? JsonResult = JsonConvert.DeserializeObject<List<string>>(result);
            if (JsonResult is null || JsonResult.Count == 0)
            {
                throw new ArgumentException("No molecules found.");
            }
            else
            {
                return JsonResult;
            }
        }


        public void Execute(object? parameter)
        {
            if (parameter is string searchText)
            {
                List<string> searchResults = GetSearchResults(searchText);
                parentApp.SwitchWindow(new SearchResultsScreen(), new SearchResultsScreenVM(searchResults, parentApp));
            }
        }
    }
}
