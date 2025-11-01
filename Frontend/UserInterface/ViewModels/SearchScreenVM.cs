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
                if (IsError ^ value != "")
                {
                    OnPropertyChanged(this, nameof(IsError));
                }
                errorMessage = value;
                OnPropertyChanged(this, nameof(ErrorMessage));
                
            }
        }
        public void SubmitText(string text)
        {
            if (text.Length < 3)
            {
                errorMessage = "Please enter at least 3 characters.";
            }
            else
            {
                errorMessage = "";
                searchCommand.Execute(text);
            }

        }

        public SearchScreenVM()
        {
            errorMessage = "";
        }

        public SearchScreenVM(SearchCommand searchCommand)
        {
            this.searchCommand = searchCommand;
        }
    }
}
