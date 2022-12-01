using Core.Services.BaseCrudService;
using App.Base;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace App.General
{
    public interface IEmployeeRepository : IBaseCrudRepository<EmployeeDto, int>
    {
	    List<EmployeeDto> GetByidSex(int idSex);
    }
}
