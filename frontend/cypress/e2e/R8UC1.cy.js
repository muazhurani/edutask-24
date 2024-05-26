describe('adding Todo item to the list of todos', () => {
  let uid;
  let name;

  before(function () {
    // Create a user for the test
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5001/users/create',
        form: true,
        body: user
      }).then((res) => {
        uid = res.body._id.$oid;
        name = user.firstName + " " + user.lastName;
      });
    });
  });

  beforeEach(function () {
    // before each test log in the user, create a task and open the task in view mode
    cy.visit('http://localhost:3000')

    cy.get('h1')
      .should('contain.text', 'Login')

    cy.get('.inputwrapper #email')
      .type('mon.doe@gmail.com')

    cy.get('form')
      .submit()

    cy.get('h1')
      .should('contain.text', 'Your tasks, Mon Doe')

    cy.get('.inputwrapper #title')
      .type(`My tasks for today`)

    cy.get('.inputwrapper #url')
      .type('https://www.youtube.com/watch?v=O6P86uwfdR0&list=WL&index=23&t=6s')

    cy.get('form')
      .submit()

    cy.get('.container-element' )
      .should('contain.text', 'My tasks for today')

    cy.contains('My tasks for today')
      .click()
  })

  it('creates a new todo item when the description field is not empty', () => {
    cy.get('form.inline-form input[type="text"]')
      .type('Complete the project report');

    cy.get('form.inline-form input[type="submit"]')
      .should('not.be.disabled')
      .click();

    cy.get('ul.todo-list')
      .should('contain.text', 'Complete the project report');
  });

  it('does not enable the "Add" button when the description field is empty', () => {
    cy.get('form.inline-form input[type="text"]')
      .should('have.value', '');

    cy.get('form.inline-form input[type="submit"]')
      .should('be.disabled');
  });

  after(function () {
    // Delete the user after tests
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5001/users/${uid}`
    }).then((res) => {
      cy.log(res.body);
    });
  });
});
