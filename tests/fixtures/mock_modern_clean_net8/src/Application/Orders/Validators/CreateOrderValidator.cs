using FluentValidation;

namespace ModernCleanApp.Application.Orders.Validators;

public record CreateOrderCommand(int CustomerId, decimal Amount);

public class CreateOrderValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderValidator()
    {
        RuleFor(x => x.CustomerId).GreaterThan(0).WithMessage("CustomerId must be positive.");
        RuleFor(x => x.Amount).GreaterThan(0).WithMessage("Amount must be greater than zero.");
    }
}
