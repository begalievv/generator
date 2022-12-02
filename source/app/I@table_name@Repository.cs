using Core.Services.BaseCrudService;
using App.Base;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace App.General
{
    public interface I@|table_name|@Repository : IBaseCrudRepository<@|table_name|@Dto, int>
    {
	    @|template_irepository|@
    }
}
