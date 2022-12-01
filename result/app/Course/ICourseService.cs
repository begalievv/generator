using System.Collections.Generic;
using Core.Services.BaseCrudService;

namespace App.General
{
    public interface IEmployeeService: IBaseCrudService<EmployeeDto, int>
    {
	    List<EmployeeDto> GetByidSex(int idSex);
    }
}