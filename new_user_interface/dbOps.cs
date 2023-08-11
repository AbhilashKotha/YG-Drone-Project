using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;

namespace UIRemote
{
    public class dbOps: DbContext
    {
        public DbSet<StepSizeValues> Parameters { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            string dbPath = "parameters.db"; // Change to your desired DB path
            optionsBuilder.UseSqlite($"Data Source={dbPath}");
            bool dbExists = File.Exists(dbPath);
        }
    }
    public class StepSizeValues
    {
        [Key]
        public int Id { get; set; }
        public String Parameter { get; set; }
        public int StepSize { get; set; }
    }
    public static class ParameterDatabaseHelper
    {
        public static void WriteParameterValues(String parameter, int value)
        {
            using (var db = new dbOps())
            {
                var parameterValues = new StepSizeValues
                {
                    Parameter = parameter,
                    StepSize = value
                };

                db.Parameters.Add(parameterValues);
                db.SaveChanges();
            }
        }
        public static int GetStepSizeByParameter(string parameter)
        {
            using (var db = new dbOps())
            {
                var stepSizeValue = db.Parameters.FirstOrDefault(p => p.Parameter == parameter);

                if (stepSizeValue != null)
                {
                    return stepSizeValue.StepSize;
                }
                else
                {
                    // Handle the case where the parameter is not found
                    throw new InvalidOperationException($"Step size value for parameter '{parameter}' not found.");
                }
            }
        }
    }
}
