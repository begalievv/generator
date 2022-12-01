using Core.Abstraction;
using App.Base;
using System;
using System.Collections.Generic;
using System.Globalization;

namespace App.General
{
    public class EmployeeDto : IDtoWithId<int>
    {
        public int id { get; set; }
public string surName { get; set; }
public string firstName { get; set; }
public string secondName { get; set; }
public int idSex { get; set; }
public DateTime? dob { get; set; }
public string strdob
{
get
{
return dob.HasValue ? dob.Value.ToString("yyyy-MM-dd") : null;
}
set
{
 dob = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);
}
}

    }
}