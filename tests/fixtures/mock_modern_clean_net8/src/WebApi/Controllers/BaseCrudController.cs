using Microsoft.AspNetCore.Mvc;

namespace ModernCleanApp.WebApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public abstract class BaseCrudController<TEntity, TDto> : ControllerBase
{
    [HttpGet]
    public virtual async Task<IActionResult> GetAll()
    {
        return Ok();
    }

    [HttpGet("{id}")]
    public virtual async Task<IActionResult> GetById(int id)
    {
        return Ok();
    }
}
