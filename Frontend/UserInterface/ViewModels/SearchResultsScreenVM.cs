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

        private string selectedMolecule;
        public SubmitCommand SubmitCommand { get { return submitCommand; } }
        public string SelectedMolecule
        { 
            get => selectedMolecule;
            set
            {
                selectedMolecule = value;
                submitCommand.OnCanExecuteChanged(this, new EventArgs());
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


        public SearchResultsScreenVM(List<string> searchResults)
        {
            this.searchResults = searchResults;
            submitCommand = new SubmitCommand(this);
            selectedMolecule = "";
        }
    }
}
