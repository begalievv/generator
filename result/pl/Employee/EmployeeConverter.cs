using App.General;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using PL.Base;

namespace PL.General
{
    public class EmployeeConverter : IModelConverter<EmployeeModel, EmployeeDto>
    {
        public EmployeeDto ToDto(EmployeeModel model)
        {
            var result = new EmployeeDto
            {
                id = model.id,
                surName = model.surName,
                firstName = model.firstName,
            };
            return result;
        }


    }
}
