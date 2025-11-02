using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserInterface
{
    public class PythonManager
    {
        private readonly string scriptPath;
        private Process pythonProcess;
        private StreamWriter pythonInput;
        public string ScriptPath => scriptPath;

        public PythonManager(string scriptPath)
        {
            this.scriptPath = scriptPath;
        }

        public void StartProcess()
        {
            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = scriptPath,
                WorkingDirectory = $"{ProjectInfo.BuildInfo.SolutionDir}/..",
                UseShellExecute = false,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = false // Change later?
            };
            pythonProcess = new Process { StartInfo = startInfo };
            pythonProcess.OutputDataReceived += (sender, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                    Trace.WriteLine("[PYTHON] " + e.Data);
            };
            pythonProcess.ErrorDataReceived += (sender, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                    Trace.WriteLine("[PYTHON-ERR] " + e.Data);
            };

            pythonProcess.Start();

            pythonProcess.BeginOutputReadLine();
            pythonProcess.BeginErrorReadLine();

            pythonInput = pythonProcess.StandardInput;
        }

        private void SendData(string data)
        {
            pythonInput.WriteLine(data);
            pythonInput.Flush();
        }

        public void DrawMolecule(string moleculeName)
        {
            if (pythonInput is null) throw new InvalidOperationException("Python process not started.");

            SendData(moleculeName);
        }

        public void StopProcess()
        {
            if (pythonInput is null) return;
            SendData("!exit");
            pythonInput.Close();
            pythonProcess.WaitForExit();
        }
    }
}
