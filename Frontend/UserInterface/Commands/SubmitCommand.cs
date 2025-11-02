using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using UserInterface.ViewModels;

namespace UserInterface.Commands
{
    public class SubmitCommand : ICommand
    {
        PythonManager pythonManager;

        public SubmitCommand(PythonManager pythonManager)
        {
            this.pythonManager = pythonManager;
        }

        public event EventHandler? CanExecuteChanged;

        public bool CanExecute(object? parameter)
        {
            return parameter is not null;
        }

        public void OnCanExecuteChanged(object sender, EventArgs e)
        {
            CanExecuteChanged?.Invoke(sender, e);
        }

        /// <summary>
        /// Runs the python script to generate the map.
        /// </summary>
        /// <param name="parameter">The name of the molecule to draw, as a <see cref="string"/>.</param>
        public void Execute(object? parameter)
        {
            if (parameter is string selectedMolecule)
            {
                try
                {
                    //ProcessStartInfo startInfo = new ProcessStartInfo
                    //{
                    //    FileName = "cmd.exe",
                    //    Arguments = $"/c python {ProjectInfo.BuildInfo.SolutionDir}/../wrapper.py {selectedMolecule}",
                    //    UseShellExecute = true,
                    //    CreateNoWindow = false,
                    //    WorkingDirectory = $"{ProjectInfo.BuildInfo.SolutionDir}/.."
                    //};
                    //Process.Start(startInfo);
                    //MessageBox.Show("Process started.");

                    pythonManager.DrawMolecule(selectedMolecule);
                }
                catch (Exception e)
                {
                    MessageBox.Show($"Execution of python script failed: {e.Message}");
                }
            }
        }
    }
}
