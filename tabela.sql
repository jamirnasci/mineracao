create table customers_training (
	RowNumber int not null,
	CustomerId int not null,
	Surname	varchar(100) not null,
	CreditScore	int not null,
	Geography varchar(100) not null,
	Gender varchar(100) not null,
	Age	int not null,
	Tenure int not null,
	Balance	decimal(10, 2) not null,
	NumOfProducts int not null,	
	HasCrCard int not null default 0,
	IsActiveMember	int not null,
	EstimatedSalary	decimal(10, 2) not null,
	Exited int not null,
  	Class varchar(100) not null
)
