using App.General;
using PL.Access;
using PL.Base;
using System;
using System.Collections.Generic;
using System.Globalization;

namespace PL.General
{
    public class EmployeeModel : BaseModel
    {
        public string surName { get; set; }
        public string firstName { get; set; }
        public string secondName { get; set; }
        public DateTime? dob { get; set; }
        public string strdob
        {
            get
            {
                return dob.HasValue ? dob.Value.ToString("yyyy-MM-dd") : null;
            }
            set
            {
                DateTime date;
                if (DateTime.TryParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out date))
                {
                    dob = date;
                }
                else
                {
                    dob = null;
                }
            }
        }
        public string contacts { get; set; }
        public int id { get; set; }
        public string userId { get; set; }
        public string email { get; set; }
        public bool? isActive { get; set; }
        public List<EmployeeRoleModel> Roles { get; set; }
        //end dictionary  

        public override bool IsNew()
        {
            return id == 0;
        }

    }
}
