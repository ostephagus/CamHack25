using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UserInterface.Commands;

namespace UserInterface.ViewModels
{
    public class SearchResultsScreenVM : ViewModelBase
    {
        private List<string> searchResults;

        private SubmitCommand submitCommand;

        private BackCommand backCommand;

        private PythonManager pythonManager;

        private string selectedMolecule;
        public SubmitCommand SubmitCommand => submitCommand;
        public BackCommand BackCommand => backCommand;
        public string SelectedMolecule
        { 
            get => selectedMolecule;
            set
            {
                selectedMolecule = value;
                submitCommand.OnCanExecuteChanged(this, new EventArgs());
                OnPropertyChanged(this, nameof(SelectedMolecule));
            }
        }

        public List<string> SearchResults
        {
            get
            {
                List<string> resultsWithBlank = searchResults;
                resultsWithBlank.Insert(0, "");
                return resultsWithBlank;
            }
        }


        public SearchResultsScreenVM(List<string> searchResults, App parentApp)
        {
            this.searchResults = searchResults;
            selectedMolecule = "";
            pythonManager = parentApp.PythonManager;
            submitCommand = new SubmitCommand(pythonManager);
            backCommand = new BackCommand(parentApp);
        }
    }
}
