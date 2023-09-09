const chai = require('chai');
const chaiHttp = require('chai-http');
const app = require('./');
const expect = chai.expect;

chai.use(chaiHttp);

describe('GET /', function() {
  it('should return Hello World!', function(done) {
    chai.request(app)
      .get('/')
      .end(function(err, res) {
        expect(res).to.have.status(200);
        expect(res.text).to.equal('Hello, World!');
        done();
      });
  });
});
