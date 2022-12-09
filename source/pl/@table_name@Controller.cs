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
    public class @|table_name|@Controller : ControllerBase
    {
        private readonly I@|table_name|@Service _@|table_name|@Service;
        private readonly IModelConverter<@|table_name|@Model, @|table_name|@Dto> _converter;

        public @|table_name|@Controller(I@|table_name|@Service service, IModelConverter<@|table_name|@Model, @|table_name|@Dto> converter)
        {
            _@|table_name|@Service = service;
            _converter = converter;
        }

        [HttpPost]
        [Route("AddOrUpdate")]
        public int AddOrUpdate(@|table_name|@Model model)
        {
            if (model.IsNew())
            {
                var addDto = _converter.ToDto(model);
                var added = _@|table_name|@Service.Add(addDto);
                return added;
            }
            else
            {
                var addDto = _converter.ToDto(model);
                var updated = _@|table_name|@Service.Update(addDto);
                return updated;
            }
        }

        [HttpGet]
        [Route("GetAll")]
        public List<@|table_name|@Dto> GetAll()
        {
            var items = _@|table_name|@Service.GetAll();
            return items;
        }

        [HttpGet]
        [Route("GetOneById")]
        public @|table_name|@Dto GetOneById(int id)
        {
            var item = _@|table_name|@Service.GetOneByKey(id);
            return item;
        }
        
        [HttpPost]
        [Route("Delete")]
        public IActionResult Delete([FromBody] int id)
        {
            _@|table_name|@Service.Remove(id);
            return Ok(new { result = "true" });
        }

        @|template_controller|@   
    }
}
