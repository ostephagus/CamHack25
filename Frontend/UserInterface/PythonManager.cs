using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserInterface
{
    public class PythonManager
    {
        private readonly string scriptPath;
        private Process pythonProcess;
        public string ScriptPath => scriptPath;

        public PythonManager(string scriptPath)
        {
            this.scriptPath = scriptPath;
        }

        public void StartProcess()
        {
            throw new NotImplementedException();
        }

        public void DrawMolecule(string moleculeName)
        {
            throw new NotImplementedException();
        }
    }
}
