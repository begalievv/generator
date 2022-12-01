using App.General;
using DAL.EF.Entities;
using System.Linq;

namespace DAL.General
{
    static partial class EmployeeDtoConverter
    {
        public static EmployeeDto ToEmployeeDto(this Employee _Employee)
        {
            var result = new EmployeeDto
            {
                id = _Employee.id,
                surName = _Employee.surName,
                firstName = _Employee.firstName,
                secondName = _Employee.secondName,

            };
            return result;
        }
        public static Employee ToEmployee(this EmployeeDto dto)
        {
            var result = new Employee
            {
                id = dto.id,
                surName = dto.surName,
                firstName = dto.firstName,
                secondName = dto.secondName,
            };
            return result;
        }
    }
}
