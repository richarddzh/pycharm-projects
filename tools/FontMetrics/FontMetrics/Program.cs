using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Unicode;
using System.Windows.Media;

namespace FontMetrics
{
    class Program
    {
        static List<string> allLine = new List<string>();
        static void Main(string[] args)
        {
            string fontPath = @"C:\Users\zhdon\Desktop\lsu.ttf";
            Uri fontUri = new Uri(fontPath);
            GlyphTypeface gt = new GlyphTypeface(fontUri);
            WriteLine("FONT_METRICS.glyphCount = {0}", gt.GlyphCount);
            WriteLine("FONT_METRICS.baseline = {0}", gt.Baseline);
            WriteLine("FONT_METRICS.capsHeight = {0}", gt.CapsHeight);
            WriteLine("FONT_METRICS.xHeight = {0}", gt.XHeight);
            WriteLine("FONT_METRICS.height = {0}", gt.Height);
            WriteLine("FONT_METRICS.glyphs = {0}", "GLYPHS");
            foreach (var kvp in gt.CharacterToGlyphMap)
            {
                var code = kvp.Key;
                var c = char.ConvertFromUtf32(code);
                var i = kvp.Value;
                const double em = 18;
                var g = gt.GetGlyphOutline(i, em, em);
                var width = (g.Bounds.Right - g.Bounds.Left) / em;
                var ascent = (0 - g.Bounds.Top) / em;
                var descent = g.Bounds.Bottom / em;
                if (double.IsInfinity(ascent) || double.IsInfinity(descent))
                {
                    continue;
                }
                WriteLine("GLYPHS[{0}] = Glyph('{1}', '{2}', {3}, {4}, {5}, {6}, {7})",
                    code,
                    c != "'" && c != "\\" ? c : "\\" + c,
                    UnicodeInfo.GetName(code).ToLower(),
                    gt.AdvanceWidths[i],
                    descent,
                    ascent,
                    gt.LeftSideBearings[i],
                    gt.RightSideBearings[i]);
            }
            Pause();
        }

        static void WriteLine(string format, params object[] args)
        {
            Console.WriteLine(format, args);
            allLine.Add(string.Format(format, args));
        }

        static void Pause()
        {
            File.WriteAllLines(@"C:\Users\zhdon\Desktop\demo.txt", allLine);
            Console.WriteLine("Press any key to exit ...");
            Console.ReadKey();
        }
    }
}
