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
#pragma warning disable CS8618
        MainWindow mainWindow;
        private UserControl currentControl;
        private ViewModelBase currentViewModel;
        private PythonManager pythonManager;
        //private string currentMolecule;
        //private List<string> searchResults;
#pragma warning restore CS8618

        public PythonManager PythonManager => pythonManager;

        private void Application_Startup(object sender, StartupEventArgs e)
        {
            mainWindow = new MainWindow();
            //MessageBox.Show($"Running in {Paths.BaseDirectory}.");
            pythonManager = new($"{Paths.BaseDirectory}/../wrapper_server.py");
            pythonManager.StartProcess();

            //currentMolecule = "";
            //searchResults = new List<string>();

            SwitchWindow(new SearchScreen(), new SearchScreenVM(new Commands.SearchCommand(this)));

            mainWindow.Show();
        }

        public void SwitchWindow(UserControl newWindow, ViewModelBase newVM)
        {
            currentControl = newWindow;
            currentViewModel = newVM;
            currentControl.DataContext = currentViewModel;
            mainWindow.SetView(currentControl);
        }

        private void Application_Exit(object sender, ExitEventArgs e)
        {
            pythonManager.StopProcess();
        }
    }

}
