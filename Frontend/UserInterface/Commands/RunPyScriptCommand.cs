using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace UserInterface.Commands
{
    class RunPyScriptCommand
    {
        private string scriptPath;
        private bool redirectOutput;

        public event EventHandler? CanExecuteChanged;

        public RunPyScriptCommand(string scriptPath, bool redirectOutput = true)
        {
            this.scriptPath = scriptPath;
            this.redirectOutput = redirectOutput;
        }

        public bool CanExecute(object? parameter)
        {
            return File.Exists(scriptPath);
        }

        public string Execute(object? parameter)
        {
            if (parameter is string sParameter)
            {
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.WindowStyle = ProcessWindowStyle.Hidden;
                startInfo.UseShellExecute = false;
                startInfo.RedirectStandardOutput = true;
                startInfo.FileName = "python.exe";
                startInfo.Arguments = $"{scriptPath} {sParameter}";
                using (Process cmdProcess = Process.Start(startInfo))
                {
                    using (StreamReader reader = cmdProcess.StandardOutput)
                    {
                        return reader.ReadToEnd();
                    }
                }
            }
            return "";
        }
    }
}
