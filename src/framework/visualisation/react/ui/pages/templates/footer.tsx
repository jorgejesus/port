interface FooterProps {
  left?: JSX.Element
  middle?: JSX.Element
  right?: JSX.Element
}

function footerLinks (): JSX.Element {
  return (
    <div className='flex flex-row gap-4 text-link font-link'>
      
      <div className=' text-primary underline'><a href='https://www.lab.uva.nl/lab/pages/privacy' target='_blank' rel='noreferrer'>Behavioural Science Lab Privacy Policy</a></div>
      <div className='bg-grey3 w-1px' />
      <div className=' text-primary underline'><a href='https://www.lab.uva.nl/lab/contact/contact' target='_blank' rel='noreferrer'>Contact</a></div>
    </div>
  )
}

export const Footer = ({ left = footerLinks(), middle, right }: FooterProps): JSX.Element => {
  return (
    <>
      <div className='bg-grey4 h-px' />
      <div className='h-full flex flex-col justify-center'>
        <div className='flex flex-row gap-4 px-14'>
          <div className='w-1/3'>
            {left}
          </div>
          <div className='w-1/3'>
            {middle}
          </div>
          <div className='w-1/3'>
            {right}
          </div>
        </div>
      </div>
    </>
  )
}
