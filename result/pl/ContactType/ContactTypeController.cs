using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using PL.ActionFilters;
using App.General;
using PL.Base;
using App.Base;
using PL.General;
using System.Collections.Generic;

namespace PL.Controllers
{
    [SessionFilter]
    [Authorize]
    [Route("api/[controller]")]
    [ApiController]
    public class EmployeeController : ControllerBase
    {
        private readonly IEmployeeService _EmployeeService;
        private readonly IModelConverter<EmployeeModel, EmployeeDto> _converter;

        public EmployeeController(IEmployeeService service,
            IModelConverter<EmployeeModel, EmployeeDto> converter,
            IEmployeeRoleService applicationRoleService
            )
        {
            _EmployeeService = service;
            _converter = converter;
        }

        [HttpPost]
        [Route("AddOrUpdate")]
        public int AddOrUpdate(EmployeeModel model)
        {
            if (model.IsNew())
            {
                var addDto = _converter.ToDto(model);
                var added = _EmployeeService.Add(addDto);
                return added;
            }
            else
            {
                var addDto = _converter.ToDto(model);
                var updated = _EmployeeService.Update(addDto);
                return updated;
            }
        }

        [HttpGet]
        [Route("GetAll")]
        public List<EmployeeDto> GetAll()
        {
            var items = _EmployeeService.GetAll();
            return items;
        }

        [HttpGet]
        [Route("GetOneById")]
        public EmployeeDto GetOneById(int id)
        {
            var item = _EmployeeService.GetOneByKey(id);
            return item;
        }

        [HttpPost]
        [Route("Delete")]
        public IActionResult Delete([FromBody] int id)
        {
            _EmployeeService.Remove(id);
            return Ok(new { result = "true" });
        }

        [HttpGet]
        [Route("GetByidSex")]
        public List<EmployeeDto> GetByidSex(int idSex)
        {
            var items = _EmployeeService.GetByidSex(idSex);
            return items;
        }
    }
}
