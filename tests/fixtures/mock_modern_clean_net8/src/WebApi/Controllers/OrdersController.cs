using Microsoft.AspNetCore.Mvc;
using ModernCleanApp.Domain.Entities;

namespace ModernCleanApp.WebApi.Controllers;

public record OrderDto(int Id, decimal Amount);

public class OrdersController : BaseCrudController<Order, OrderDto>
{
    [HttpPost("submit")]
    public async Task<IActionResult> SubmitOrder(
        [FromBody] OrderDto dto,
        CancellationToken cancellationToken)
    {
        return Ok(dto);
    }
}
