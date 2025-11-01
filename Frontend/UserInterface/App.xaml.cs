using System.Configuration;
using System.Data;
using System.Windows;
using System.Windows.Controls;
using UserInterface.Views;
using UserInterface.ViewModels;

namespace UserInterface
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        MainWindow mainWindow;
        private UserControl currentControl;
        private ViewModelBase currentViewModel;

        private void Application_Startup(object sender, StartupEventArgs e)
        {
            mainWindow = new MainWindow();

            SwitchWindow(new Views.SearchScreen(), new SearchScreenVM(new Commands.SearchCommand(this)));

            mainWindow.Show();
        }

        public void SwitchWindow(UserControl newWindow, ViewModelBase newVM)
        {
            currentControl = newWindow;
            currentViewModel = newVM;
            currentControl.DataContext = currentViewModel;
            mainWindow.SetView(currentControl);
        }
    }

}
