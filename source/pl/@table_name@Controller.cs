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
        public int Create(@|table_name|@Model model)
        {
            var addDto = _converter.ToDto(model);
            var added = _@|table_name|@Service.Add(addDto);
            return added;
        }

        [HttpPut]
        [Route("{id:int}")]
        public int Update(int id, @|table_name|@Model model)
        {
            var addDto = _converter.ToDto(model);
            var updated = _@|table_name|@Service.Update(addDto);
            return updated;
        }

        [HttpDelete]
        [Route("{id:int}")]
        public IActionResult Delete(int id)
        {
            _@|table_name|@Service.Remove(id);
            return Ok(new { result = "true" });
        }

        [HttpGet]
        [Route("{id:int}")]
        public @|table_name|@Dto GetOneById(int id)
        {
            var item = _@|table_name|@Service.GetOneByKey(id);
            return item;
        }

        [HttpGet]
        [Route("GetAll")]
        public List<@|table_name|@Dto> GetAll()
        {
            var items = _@|table_name|@Service.GetAll();
            return items;
        }

        @|template_controller|@   
    }
}
