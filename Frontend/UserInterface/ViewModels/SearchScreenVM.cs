using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;

using UserInterface.Commands;

namespace UserInterface.ViewModels
{
    public class SearchScreenVM : ViewModelBase
    {
        private string errorMessage;
        private static string DEFAULT_ERR_MESSAGE = "An error occurred.";
        private SearchCommand searchCommand;

        public bool IsError
        {
            get => errorMessage != "";
            set
            {
                if (value)
                {
                    errorMessage = DEFAULT_ERR_MESSAGE;
                }
            }
        }

        public string ErrorMessage
        {
            get => errorMessage;
            set
            {
                errorMessage = value;
                OnPropertyChanged(this, nameof(ErrorMessage));
                OnPropertyChanged(this, nameof(IsError));
                
            }
        }
        public void SubmitText(string text)
        {
            if (text.Length < 3)
            {
                ErrorMessage = "Please enter at least 3 characters.";
            }
            else
            {
                ErrorMessage = "";
                try
                {
                    searchCommand.Execute(text);
                }
                catch (ArgumentException e)
                {
                    ErrorMessage = "No results. Try again with a different molecule.";
                }
            }

        }

        public SearchScreenVM()
        {
            errorMessage = "";
        }

        public SearchScreenVM(SearchCommand searchCommand)
        {
            this.searchCommand = searchCommand;
            errorMessage = "";
        }
    }
}
