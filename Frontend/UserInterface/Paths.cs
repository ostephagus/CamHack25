using ProjectInfo;
using System.IO;

namespace UserInterface
{
    public static class Paths
    {
        public static string BaseDirectory
        {
            get
            {
                string dir = BuildInfo.SolutionDir;
                if (string.IsNullOrEmpty(dir) || !Directory.Exists(dir))
                {
                    return AppDomain.CurrentDomain.BaseDirectory;
                }
                else
                {
                    return dir;
                }
            }
        }
    }
}
