using System.Collections.Generic;
using Core.Services.BaseCrudService;

namespace App.General
{
    public interface I@|table_name|@Service: IBaseCrudService<@|table_name|@Dto, int>
    {
	    @|template_iservice|@
    }
}