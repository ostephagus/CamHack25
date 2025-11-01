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
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.WindowStyle = ProcessWindowStyle.Hidden;
            startInfo.FileName = "python.exe";
            startInfo.Arguments = $"../../../../../api_calls/spell_suggest.py {searchText}";
            startInfo.UseShellExecute = false;
            startInfo.RedirectStandardOutput = true;

            List<string> searchResults = new List<string>();
            using (Process cmdProcess = Process.Start(startInfo))
            {
                using (StreamReader reader = cmdProcess.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    return JsonConvert.DeserializeObject<List<string>>(result);
                }
            }
        }


        public void Execute(object? parameter)
        {
            if (parameter is string searchText)
            {
                List<string> searchResults = GetSearchResults(searchText);
                parentApp.SwitchWindow(new SearchResultsScreen(), new SearchResultsScreenVM(searchResults));
            }
        }
    }
}
