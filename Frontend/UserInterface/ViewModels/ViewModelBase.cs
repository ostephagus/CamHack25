using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserInterface.ViewModels
{
    public class ViewModelBase
    {
        public event PropertyChangedEventHandler? PropertyChanged;
        protected void OnPropertyChanged(object? sender, string propertyName)
        {
            PropertyChanged?.Invoke(sender, new PropertyChangedEventArgs(propertyName));
        }
    }
}
